from fastapi import FastAPI, UploadFile, File, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import sys
import shutil
from PIL import Image
import uuid
import time
from base64 import b64encode
import asyncio

# Import cryptography phases
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

app = FastAPI(title="CipherNet Backend API")

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
    content = await file.read()
    key_16 = os.urandom(16)
    key_24 = DES3.adjust_key_parity(os.urandom(24))
    
    start = time.perf_counter()
    aes_iv, aes_ct = encrypt_aes_cbc(key_16, content)
    aes_time = time.perf_counter() - start
    
    start = time.perf_counter()
    des_iv, des_ct = encrypt_3des_cbc(key_24, content)
    des_time = time.perf_counter() - start
    
    return {
        "filename": file.filename,
        "aes_time": f"{aes_time:.6f}",
        "des_time": f"{des_time:.6f}"
    }

@app.post("/api/encrypt/image")
async def encrypt_image(file: UploadFile = File(...)):
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
            return "data:image/bmp;base64," + b64encode(img_file.read()).decode('utf-8')
            
    res = {
        "ecb": get_b64(ecb_path),
        "cbc": get_b64(cbc_path)
    }
    
    for p in [orig_path, bmp_path, ecb_path, cbc_path]:
        if os.path.exists(p): os.remove(p)
    return res

class AvalancheRequest(BaseModel):
    plaintext: str

@app.post("/api/phase1/avalanche")
async def avalanche_effect(req: AvalancheRequest):
    key = os.urandom(16)
    plaintext = req.plaintext.encode('utf-8')
    if not plaintext: plaintext = b"Sample text"
        
    iv1, ciphertext1 = encrypt_aes_cbc(key, plaintext)
    
    plaintext_altered = flip_bit(plaintext, 0, 0)
    cipher_pt = AES.new(key, AES.MODE_CBC, iv=iv1)
    ciphertext2 = cipher_pt.encrypt(pad(plaintext_altered, AES.block_size))
    
    total_bits = len(ciphertext1) * 8
    diff_pt = count_bit_differences(ciphertext1, ciphertext2)
    
    return {
        "pt_diff_percent": round((diff_pt / total_bits) * 100, 2)
    }

# ----------------- PHASE 2 -----------------
@app.get("/api/phase2/rsa-hybrid")
async def rsa_hybrid():
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

@app.get("/api/phase2/dh-mitm")
async def dh_mitm():
    parameters = dh.generate_parameters(generator=2, key_size=512)
    alice = DHParticipant(parameters)
    bob = DHParticipant(parameters)
    eve = DHParticipant(parameters)
    
    alice_secret = alice.generate_shared_secret(bob.public_key)
    bob_secret = bob.generate_shared_secret(alice.public_key)
    
    alice_eve_secret = alice.generate_shared_secret(eve.public_key)
    bob_eve_secret = bob.generate_shared_secret(eve.public_key)
    
    return {
        "alice_secret": alice_secret.hex()[:32] + "...",
        "bob_secret": bob_secret.hex()[:32] + "...",
        "match": alice_secret == bob_secret,
        "mitm_alice": alice_eve_secret.hex()[:32] + "...",
        "mitm_bob": bob_eve_secret.hex()[:32] + "..."
    }

# ----------------- PHASE 3 -----------------
class HashRequest(BaseModel):
    data: str

@app.post("/api/phase3/hash")
async def compute_hash(req: HashRequest):
    return {"hash": compute_sha256(req.data.encode('utf-8'))}

class TamperRequest(BaseModel):
    data: str
    tamper_index: int

@app.post("/api/phase3/tamper")
async def tamper_detect(req: TamperRequest):
    original = req.data.encode('utf-8')
    orig_hash = compute_sha256(original)
    
    idx = req.tamper_index % len(original) if len(original) > 0 else 0
    tampered = bytearray(original)
    if tampered: tampered[idx] ^= 0xFF
    tampered = bytes(tampered)
    
    tamp_hash = compute_sha256(tampered)
    return {
        "original_hash": orig_hash,
        "tampered_data": tampered.decode('utf-8', errors='replace'),
        "tampered_hash": tamp_hash,
        "match": orig_hash == tamp_hash
    }

# ----------------- PHASE 4 -----------------
@app.post("/api/phase4/sign")
async def api_sign(req: HashRequest):
    priv, pub = generate_rsa_keypair(2048)
    data = req.data.encode('utf-8')
    sig = sign_data(priv, data)
    is_valid = verify_signature(pub, data, sig)
    return {
        "signature": sig.hex()[:64] + "...",
        "valid": is_valid
    }

@app.get("/api/phase4/cert")
async def get_cert():
    cert_pem, _ = generate_self_signed_cert()
    from cryptography.x509 import load_pem_x509_certificate
    cert = load_pem_x509_certificate(cert_pem)
    return {
        "subject": cert.subject.rfc4514_string(),
        "issuer": cert.issuer.rfc4514_string(),
        "valid_from": str(cert.not_valid_before_utc),
        "valid_until": str(cert.not_valid_after_utc),
        "pem": cert_pem.decode('utf-8')
    }

# ----------------- PHASE 5 -----------------
@app.websocket("/ws/simulate")
async def websocket_simulate(websocket: WebSocket):
    await websocket.accept()
    async def log(role, msg):
        await websocket.send_json({"role": role, "message": msg})
        await asyncio.sleep(0.8)

    try:
        await log("server", "Generating RSA keypair...")
        uni_priv_rsa, uni_pub_rsa = generate_rsa_keypair(1024)
        
        transcript_data = b"Student: John Doe\nGrades: A, B, A, C"
        
        await log("client", "[+] Connected to University Server.")
        await log("server", "[Phase 4] Kerberos Auth OK: STUDENT_987654321")
        
        await log("server", "\n[Phase 2] Initiating DH Exchange...")
        parameters = dh.generate_parameters(generator=2, key_size=512)
        uni_dh = DHParticipant(parameters)
        student_dh = DHParticipant(parameters)
        
        uni_shared = uni_dh.generate_shared_secret(student_dh.public_key)
        student_shared = student_dh.generate_shared_secret(uni_dh.public_key)
        
        await log("server", f"Shared Secret derived (hex): {uni_shared.hex()[:16]}...")
        
        transcript_hash = compute_sha256(transcript_data)
        signature = sign_data(uni_priv_rsa, transcript_hash.encode())
        
        await log("server", "\n[Phase 1] Encrypting Transcript with AES...")
        aes_key = uni_shared[:16] 
        iv, ciphertext = encrypt_aes_cbc(aes_key, transcript_data)
        
        await log("server", "Sending Encrypted Package to Student...")
        await log("client", "\n[Phase 1] Decrypting Transcript...")
        
        plaintext = decrypt_aes_cbc(student_shared[:16], iv, ciphertext)
        await log("client", f"Decrypted Data: {plaintext.decode(errors='ignore')}")
        
        current_hash = compute_sha256(plaintext)
        if current_hash == transcript_hash:
            await log("client", "-> [Phase 3] Integrity PASSED!")
            
        if verify_signature(uni_pub_rsa, transcript_hash.encode(), signature):
            await log("client", "-> [Phase 4] Signature PASSED!")
            
        await log("server", "\n=== TRANSMISSION COMPLETE ===")
        
    except WebSocketDisconnect:
        pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
