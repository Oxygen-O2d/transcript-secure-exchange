import socket
import sys
import os
import json
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import decrypt_aes_cbc
from phase2_asymmetric.dh_exchange import DHParticipant
from phase3_integrity.hashing import verify_hash, compute_sha256
from phase4_authentication.digital_signature import verify_signature

HOST = '127.0.0.1'
PORT = 65432

def start_client():
    print("=== STUDENT (RECEIVER) CLIENT STARTING ===")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to University Server.")
        
        s.sendall(b"KERBEROS_OK")
        
        param_bytes = s.recv(2048)
        parameters = serialization.load_pem_parameters(param_bytes)
        
        student_dh = DHParticipant(parameters)
        
        uni_dh_pub_bytes = s.recv(1024)
        uni_pub_key = serialization.load_pem_public_key(uni_dh_pub_bytes)
        
        student_dh_pub_bytes = student_dh.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        s.sendall(student_dh_pub_bytes)
        
        shared_secret = student_dh.generate_shared_secret(uni_pub_key)
        print(f"Derived Shared Secret (hex): {shared_secret.hex()}")
        
        uni_pub_rsa = s.recv(1024)
        
        payload_bytes = s.recv(4096)
        payload = json.loads(payload_bytes.decode())
        
        iv = bytes.fromhex(payload['iv'])
        ciphertext = bytes.fromhex(payload['ciphertext'])
        signature = bytes.fromhex(payload['signature'])
        expected_hash = payload['original_hash']
        
        print("\n[Phase 1] Decrypting Transcript...")
        aes_key = shared_secret[:16]
        try:
            plaintext = decrypt_aes_cbc(aes_key, iv, ciphertext)
            print(f"Decrypted Data Preview: {plaintext[:50]}")
        except Exception as e:
            print(f"Decryption failed: {e}")
            return
            
        print("\n[Phase 3] Verifying Integrity...")
        current_hash = compute_sha256(plaintext)
        if current_hash == expected_hash:
            print(f"Integrity check PASSED. Hash matches: {current_hash}")
        else:
            print(f"Integrity check FAILED!\nExpected: {expected_hash}\nGot:      {current_hash}")
            
        print("\n[Phase 4] Verifying Digital Signature...")
        is_valid_sig = verify_signature(uni_pub_rsa, expected_hash.encode(), signature)
        if is_valid_sig:
            print("Signature verification PASSED. Sender is authenticated.")
        else:
            print("Signature verification FAILED! Sender could not be authenticated.")
            
        print("=== STUDENT (RECEIVER) FINISHED ===")

if __name__ == "__main__":
    start_client()
