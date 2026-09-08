from fastapi import FastAPI, UploadFile, File, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import os
import sys
import shutil
from PIL import Image
import uuid
import time
from base64 import b64encode

# Add parent dir to path to import phase modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc, encrypt_3des_cbc, decrypt_aes_cbc
from phase1_symmetric.ecb_vs_cbc import encrypt_image_ecb, encrypt_image_cbc
from phase2_asymmetric.dh_exchange import DHParticipant
from phase2_asymmetric.rsa_hybrid import generate_rsa_keypair
from phase3_integrity.hashing import compute_sha256
from phase4_authentication.digital_signature import sign_data, verify_signature
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
import json
import asyncio

app = FastAPI(title="Secure Transcript Exchange API")

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TEMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp")
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

@app.post("/api/encrypt/file")
async def encrypt_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        
        key_16 = os.urandom(16)
        key_24 = os.urandom(24)
        
        # AES
        start = time.perf_counter()
        aes_iv, aes_ct = encrypt_aes_cbc(key_16, content)
        aes_time = time.perf_counter() - start
        
        # 3DES
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
        # Create unique ID for this request to avoid collisions
        req_id = str(uuid.uuid4())
        
        orig_path = os.path.join(TEMP_DIR, f"{req_id}_orig.png")
        bmp_path = os.path.join(TEMP_DIR, f"{req_id}_target.bmp")
        ecb_path = os.path.join(TEMP_DIR, f"{req_id}_ecb.bmp")
        cbc_path = os.path.join(TEMP_DIR, f"{req_id}_cbc.bmp")
        
        # Save uploaded file
        with open(orig_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Convert to BMP for encryption
        with Image.open(orig_path) as img:
            img = img.convert("RGB")
            img.save(bmp_path, format="BMP")
            
        key = os.urandom(16)
        iv = os.urandom(16)
        
        # Encrypt
        encrypt_image_ecb(bmp_path, ecb_path, key)
        encrypt_image_cbc(bmp_path, cbc_path, key, iv)
        
        # Function to read and encode image to base64
        def get_b64(path):
            with open(path, "rb") as img_file:
                return b64encode(img_file.read()).decode('utf-8')
                
        # Send back original as png, but encrypted as bmp
        res = {
            "original": f"data:image/png;base64,{get_b64(orig_path)}",
            "ecb": f"data:image/bmp;base64,{get_b64(ecb_path)}",
            "cbc": f"data:image/bmp;base64,{get_b64(cbc_path)}"
        }
        
        # Cleanup
        for p in [orig_path, bmp_path, ecb_path, cbc_path]:
            if os.path.exists(p):
                os.remove(p)
                
        return JSONResponse(content=res)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
            log("server", "Error: transcript.txt not found.")
            return
            
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
