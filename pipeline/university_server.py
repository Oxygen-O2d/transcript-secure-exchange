import socket
import sys
import os
import time
import json
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc
from phase2_asymmetric.dh_exchange import DHParticipant
from phase2_asymmetric.rsa_hybrid import generate_rsa_keypair, rsa_encrypt_session_key
from phase3_integrity.hashing import compute_sha256
from phase4_authentication.digital_signature import sign_data
from phase4_authentication.kerberos_mock import simulate_kerberos_gate
from phase4_authentication.certificate import generate_self_signed_cert

HOST = '127.0.0.1'
PORT = 65432

def start_server(simulate_mitm=False, simulate_tamper=False):
    print("=== UNIVERSITY (SENDER) SERVER STARTING ===")
    
    cert_pem, priv_pem = generate_self_signed_cert()
    uni_priv_rsa, uni_pub_rsa = generate_rsa_keypair()
    
    transcript_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transcript.txt')
    if not os.path.exists(transcript_path):
        print("Error: transcript.txt not found. Run generate_mock_data.py")
        return
        
    with open(transcript_path, 'rb') as f:
        transcript_data = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"University Server listening on {HOST}:{PORT}")
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            
            kerberos_passed = conn.recv(1024)
            if kerberos_passed == b"KERBEROS_OK":
                simulate_kerberos_gate("STUDENT_987654321")
            
            # Phase 2: DH Key Exchange
            print("\n[Phase 2] Initiating DH Exchange...")
            parameters = dh.generate_parameters(generator=2, key_size=512)
            conn.sendall(parameters.parameter_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.ParameterFormat.PKCS3
            ))
            
            uni_dh = DHParticipant(parameters)
            uni_dh_pub_bytes = uni_dh.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            conn.sendall(uni_dh_pub_bytes)
            
            student_dh_pub_bytes = conn.recv(1024)
            student_pub_key = serialization.load_pem_public_key(student_dh_pub_bytes)
            
            if simulate_mitm:
                print("MITM NOT IMPLEMENTED IN SOCKET FULLY FOR THIS DEMO. See mitm_attack.py")
                
            shared_secret = uni_dh.generate_shared_secret(student_pub_key)
            print(f"Derived Shared Secret (hex): {shared_secret.hex()}")
            
            # Send RSA pub key for hybrid encrypt
            conn.sendall(uni_pub_rsa)
            
            # Phase 3 & 4: Integrity and Signatures
            transcript_hash = compute_sha256(transcript_data)
            signature = sign_data(uni_priv_rsa, transcript_hash.encode())
            
            if simulate_tamper:
                print("\n[Phase 3] Tampering with transcript data!")
                transcript_data = transcript_data.replace(b"Grade: A", b"Grade: F")
            
            print(f"\n[Phase 1] Encrypting Transcript with AES using Shared Secret...")
            aes_key = shared_secret[:16] 
            iv, ciphertext = encrypt_aes_cbc(aes_key, transcript_data)
            
            payload = {
                'iv': iv.hex(),
                'ciphertext': ciphertext.hex(),
                'signature': signature.hex(),
                'original_hash': transcript_hash
            }
            
            print("Sending Encrypted Package to Student...")
            conn.sendall(json.dumps(payload).encode())
            print("=== UNIVERSITY (SENDER) FINISHED ===")

if __name__ == "__main__":
    simulate_tamper = '--tamper' in sys.argv
    start_server(simulate_tamper=simulate_tamper)
