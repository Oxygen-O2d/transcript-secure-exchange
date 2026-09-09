from fastapi import FastAPI, UploadFile, File, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import os
import sys
import shutil
from PIL import Image
import uuid
import time
from base64 import b64encode

# Add parent dir to path to import phase modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc, encrypt_3des_cbc, decrypt_aes_cbc, decrypt_3des_cbc
from phase1_symmetric.ecb_vs_cbc import encrypt_image_ecb, encrypt_image_cbc
from phase1_symmetric.avalanche import flip_bit, count_bit_differences
from phase2_asymmetric.dh_exchange import DHParticipant
from phase2_asymmetric.rsa_hybrid import generate_rsa_keypair, rsa_encrypt_session_key, rsa_decrypt_session_key
from phase3_integrity.hashing import compute_sha256, verify_hash
from phase4_authentication.digital_signature import sign_data, verify_signature
from phase4_authentication.certificate import generate_self_signed_cert
from cryptography.hazmat.primitives.asymmetric import dh
from Crypto.Cipher import AES, DES3
from Crypto.Util.Padding import pad
import json
import asyncio

app = FastAPI(title="Secure Transcript Exchange API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

# ----------------- PHASE 1 -----------------

@app.post("/api/encrypt/file")
async def encrypt_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        key_16 = os.urandom(16)
        key_24 = os.urandom(24)
        
        start = time.perf_counter()
        aes_iv, aes_ct = encrypt_aes_cbc(key_16, content)
        aes_time = time.perf_counter() - start
        
        start = time.perf_counter()
        des_iv, des_ct = encrypt_3des_cbc(key_24, content)
        des_time = time.perf_counter() - start
        
        return {
            "filename": file.filename,
            "original_size": len(content),
            "aes_time": f"{aes_time:.6f}",
            "des_time": f"{des_time:.6f}",
            "aes_size": len(aes_iv + aes_ct),
            "des_size": len(des_iv + des_ct)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/encrypt/image")
async def encrypt_image(file: UploadFile = File(...)):
    try:
        req_id = str(uuid.uuid4())
        orig_path = os.path.join(TEMP_DIR, f"{req_id}_orig.png")
        bmp_path = os.path.join(TEMP_DIR, f"{req_id}_target.bmp")
        ecb_path = os.path.join(TEMP_DIR, f"{req_id}_ecb.bmp")
        cbc_path = os.path.join(TEMP_DIR, f"{req_id}_cbc.bmp")
        
        with open(orig_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        with Image.open(orig_path) as img:
            img = img.convert("RGB")
            img.save(bmp_path, format="BMP")
            
        key = os.urandom(16)
        iv = os.urandom(16)
        
        encrypt_image_ecb(bmp_path, ecb_path, key)
        encrypt_image_cbc(bmp_path, cbc_path, key, iv)
        
        def get_b64(path):
            with open(path, "rb") as img_file:
                return b64encode(img_file.read()).decode('utf-8')
                
        res = {
            "original": f"data:image/png;base64,{get_b64(orig_path)}",
            "ecb": f"data:image/bmp;base64,{get_b64(ecb_path)}",
            "cbc": f"data:image/bmp;base64,{get_b64(cbc_path)}"
        }
        
        for p in [orig_path, bmp_path, ecb_path, cbc_path]:
            if os.path.exists(p): os.remove(p)
        return JSONResponse(content=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AvalancheRequest(BaseModel):
    plaintext: str

@app.post("/api/phase1/avalanche")
async def avalanche_effect(req: AvalancheRequest):
    try:
        key = os.urandom(16)
        plaintext = req.plaintext.encode('utf-8')
        if len(plaintext) == 0:
            plaintext = b"Sample text for avalanche effect."
            
        iv1, ciphertext1 = encrypt_aes_cbc(key, plaintext)
        
        plaintext_altered = flip_bit(plaintext, 0, 0)
        cipher_pt = AES.new(key, AES.MODE_CBC, iv=iv1)
        ciphertext2 = cipher_pt.encrypt(pad(plaintext_altered, AES.block_size))
        
        key_altered = flip_bit(key, 0, 0)
        cipher_key = AES.new(key_altered, AES.MODE_CBC, iv=iv1)
        ciphertext3 = cipher_key.encrypt(pad(plaintext, AES.block_size))
        
        total_bits = len(ciphertext1) * 8
        diff_pt = count_bit_differences(ciphertext1, ciphertext2)
        diff_key = count_bit_differences(ciphertext1, ciphertext3)
        
        return {
            "total_bits": total_bits,
            "pt_diff_bits": diff_pt,
            "pt_diff_percent": round((diff_pt / total_bits) * 100, 2),
            "key_diff_bits": diff_key,
            "key_diff_percent": round((diff_key / total_bits) * 100, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/phase1/benchmark")
async def benchmark():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sizes = ['10kb', '100kb', '1mb']
        results = []
        aes_key = os.urandom(16)
        des3_key = DES3.adjust_key_parity(os.urandom(24))
        
        for size in sizes:
            file_path = os.path.join(base_dir, 'data', f'test_{size}.txt')
            if not os.path.exists(file_path):
                # If mock data doesn't exist, create it in memory for the benchmark
                num_bytes = 10 * 1024 if size == '10kb' else 100 * 1024 if size == '100kb' else 1024 * 1024
                data = os.urandom(num_bytes)
            else:
                with open(file_path, 'rb') as f:
                    data = f.read()
                    
            start = time.perf_counter()
            iv, ct = encrypt_aes_cbc(aes_key, data)
            aes_enc_time = time.perf_counter() - start
            
            start = time.perf_counter()
            decrypt_aes_cbc(aes_key, iv, ct)
            aes_dec_time = time.perf_counter() - start
            
            start = time.perf_counter()
            iv3, ct3 = encrypt_3des_cbc(des3_key, data)
            des3_enc_time = time.perf_counter() - start
            
            start = time.perf_counter()
            decrypt_3des_cbc(des3_key, iv3, ct3)
            des3_dec_time = time.perf_counter() - start
            
            results.append({
                "size": size,
                "aes_enc": round(aes_enc_time, 6),
                "aes_dec": round(aes_dec_time, 6),
                "des3_enc": round(des3_enc_time, 6),
                "des3_dec": round(des3_dec_time, 6),
            })
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------- PHASE 2 -----------------

@app.get("/api/phase2/dh-mitm")
async def dh_mitm():
    try:
        # standard DH
        parameters = dh.generate_parameters(generator=2, key_size=512)
        alice = DHParticipant(parameters)
        bob = DHParticipant(parameters)
        eve = DHParticipant(parameters)
        
        alice_secret = alice.generate_shared_secret(bob.public_key)
        bob_secret = bob.generate_shared_secret(alice.public_key)
        
        # MITM
        alice_eve_secret = alice.generate_shared_secret(eve.public_key)
        eve_alice_secret = eve.generate_shared_secret(alice.public_key)
        
        bob_eve_secret = bob.generate_shared_secret(eve.public_key)
        eve_bob_secret = eve.generate_shared_secret(bob.public_key)
        
        return {
            "secure": {
                "alice_secret": alice_secret.hex(),
                "bob_secret": bob_secret.hex(),
                "match": alice_secret == bob_secret
            },
            "mitm": {
                "alice_thinks_secret_is": alice_eve_secret.hex(),
                "bob_thinks_secret_is": bob_eve_secret.hex(),
                "eve_secret_with_alice": eve_alice_secret.hex(),
                "eve_secret_with_bob": eve_bob_secret.hex(),
                "alice_bob_match": alice_eve_secret == bob_eve_secret
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/phase2/rsa-hybrid")
async def rsa_hybrid():
    try:
        priv, pub = generate_rsa_keypair(2048)
        aes_session_key = os.urandom(16)
        
        enc_key = rsa_encrypt_session_key(pub, aes_session_key)
        dec_key = rsa_decrypt_session_key(priv, enc_key)
        
        return {
            "original_key": aes_session_key.hex(),
            "encrypted_key_preview": enc_key[:16].hex() + "...",
            "decrypted_key": dec_key.hex(),
            "match": aes_session_key == dec_key
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------- PHASE 3 -----------------

class HashRequest(BaseModel):
    data: str

@app.post("/api/phase3/hash")
async def compute_hash(req: HashRequest):
    try:
        h = compute_sha256(req.data)
        return {"hash": h}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class TamperRequest(BaseModel):
    data: str
    tamper_index: int

@app.post("/api/phase3/tamper-detect")
async def tamper_detect(req: TamperRequest):
    try:
        original = req.data.encode('utf-8')
        if len(original) == 0:
            original = b"Genuine data."
        
        orig_hash = compute_sha256(original)
        
        idx = req.tamper_index % len(original) if len(original) > 0 else 0
        
        tampered = bytearray(original)
        if len(tampered) > 0:
            tampered[idx] ^= 0xFF
        tampered = bytes(tampered)
        
        tamp_hash = compute_sha256(tampered)
        
        return {
            "original_data": original.decode('utf-8', errors='ignore'),
            "original_hash": orig_hash,
            "tampered_data": tampered.decode('utf-8', errors='ignore'),
            "tampered_hash": tamp_hash,
            "match": orig_hash == tamp_hash
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------- PHASE 4 -----------------

class SignRequest(BaseModel):
    data: str

@app.post("/api/phase4/digital-signature")
async def api_digital_signature(req: SignRequest):
    try:
        priv, pub = generate_rsa_keypair(2048)
        data = req.data.encode('utf-8')
        
        sig = sign_data(priv, data)
        
        is_valid = verify_signature(pub, data, sig)
        
        tampered_data = b"T" + data[1:] if len(data) > 1 else b"Fake"
        is_valid_tampered = verify_signature(pub, tampered_data, sig)
        
        return {
            "signature_preview": sig[:16].hex() + "...",
            "valid_original": is_valid,
            "tampered_data": tampered_data.decode('utf-8', errors='ignore'),
            "valid_tampered": is_valid_tampered
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/phase4/certificate")
async def get_certificate():
    try:
        cert_pem, priv_pem = generate_self_signed_cert()
        # Parse it a bit to show details
        from cryptography.x509 import load_pem_x509_certificate
        cert = load_pem_x509_certificate(cert_pem)
        
        return {
            "cert_pem": cert_pem.decode('utf-8'),
            "subject": str(cert.subject),
            "issuer": str(cert.issuer),
            "serial_number": cert.serial_number,
            "not_valid_before": str(cert.not_valid_before_utc),
            "not_valid_after": str(cert.not_valid_after_utc)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/phase4/kerberos")
async def get_kerberos():
    try:
        steps = [
            "Client (Student 987654321) requests Ticket Granting Ticket (TGT) from Authentication Server (AS).",
            "AS verifies Student identity in database and issues encrypted TGT.",
            "Client sends TGT to Ticket Granting Server (TGS) requesting access to Transcript Service.",
            "TGS verifies TGT, issues Service Ticket for Transcript Service.",
            "Client presents Service Ticket to Transcript Server.",
            "Transcript Server verifies Service Ticket. Access GRANTED."
        ]
        return {"steps": steps}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------- PHASE 5 -----------------

@app.websocket("/ws/simulate")
async def websocket_simulate(websocket: WebSocket):
    await websocket.accept()
    try:
        def log(role, msg):
            asyncio.create_task(websocket.send_json({"role": role, "message": msg}))

        log("server", "=== SERVER STARTING ===")
        log("client", "=== CLIENT STARTING ===")
        await asyncio.sleep(0.5)

        log("server", "Generating RSA keypair...")
        uni_priv_rsa, uni_pub_rsa = generate_rsa_keypair()
        await asyncio.sleep(0.5)
        
        transcript_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transcript.txt')
        if not os.path.exists(transcript_path):
            with open(transcript_path, 'w') as f:
                f.write("Student: John Doe\nID: 987654321\nGrades: A, B, A, C")
            
        with open(transcript_path, 'rb') as f:
            transcript_data = f.read()

        log("server", "Listening on 127.0.0.1:65432... Waiting for student connection.")
        await asyncio.sleep(0.5)
        log("client", "[+] Connected to University Server.")
        log("server", "[+] Connected by ('127.0.0.1', 54321)")
        await asyncio.sleep(0.5)

        log("client", "Sending Kerberos Ticket...")
        log("server", "[Phase 4] Kerberos Auth OK: STUDENT_987654321")
        await asyncio.sleep(0.5)

        log("server", "\n[Phase 2] Initiating DH Exchange...")
        parameters = dh.generate_parameters(generator=2, key_size=512)
        uni_dh = DHParticipant(parameters)
        log("server", "Sending DH Parameters and Public Key...")
        await asyncio.sleep(0.5)

        student_dh = DHParticipant(parameters)
        log("client", "Received DH Parameters. Sending Public Key...")
        await asyncio.sleep(0.5)

        uni_pub_key = uni_dh.public_key
        student_pub_key = student_dh.public_key

        uni_shared = uni_dh.generate_shared_secret(student_pub_key)
        student_shared = student_dh.generate_shared_secret(uni_pub_key)
        
        log("server", f"Shared Secret derived (hex): {uni_shared.hex()[:16]}...")
        log("client", f"Shared Secret derived (hex): {student_shared.hex()[:16]}...")
        await asyncio.sleep(0.5)

        transcript_hash = compute_sha256(transcript_data)
        signature = sign_data(uni_priv_rsa, transcript_hash.encode())
        
        log("server", "\n[Phase 1] Encrypting Transcript with AES...")
        aes_key = uni_shared[:16] 
        iv, ciphertext = encrypt_aes_cbc(aes_key, transcript_data)
        
        log("server", "Sending Encrypted Package to Student...")
        await asyncio.sleep(0.5)

        log("client", "\n[Phase 1] Decrypting Transcript...")
        client_aes_key = student_shared[:16]
        plaintext = decrypt_aes_cbc(client_aes_key, iv, ciphertext)
        
        preview = plaintext[:40].decode(errors='ignore').replace('\n', ' ')
        log("client", f"Decrypted Preview: {preview}...")
        await asyncio.sleep(0.5)
            
        log("client", "\n[Phase 3] Verifying Integrity...")
        current_hash = compute_sha256(plaintext)
        if current_hash == transcript_hash:
            log("client", "-> Integrity PASSED! Hash matches.")
        else:
            log("client", "-> Integrity FAILED!")
        await asyncio.sleep(0.5)
            
        log("client", "\n[Phase 4] Verifying Signature...")
        is_valid_sig = verify_signature(uni_pub_rsa, transcript_hash.encode(), signature)
        if is_valid_sig:
            log("client", "-> Signature PASSED! Authentic Sender.")
        else:
            log("client", "-> Signature FAILED!")
            
        log("server", "\n=== TRANSMISSION COMPLETE ===")
        log("client", "\n=== TRANSCRIPT RECEIVED SUCCESSFULLY ===")

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"Simulation Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
