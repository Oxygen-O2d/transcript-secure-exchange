import customtkinter as ctk
import socket
import threading
import sys
import os
import json
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc
from phase2_asymmetric.dh_exchange import DHParticipant
from phase2_asymmetric.rsa_hybrid import generate_rsa_keypair
from phase3_integrity.hashing import compute_sha256
from phase4_authentication.digital_signature import sign_data
from phase4_authentication.certificate import generate_self_signed_cert

HOST = '127.0.0.1'
PORT = 65432

class ServerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("University Server (Sender)")
        self.geometry("600x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header = ctk.CTkLabel(self, text="University Transcript Server", font=("Arial", 20, "bold"))
        self.header.grid(row=0, column=0, pady=10)
        
        self.log_box = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 12))
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.start_btn = ctk.CTkButton(self, text="Start Listening", command=self.start_server_thread)
        self.start_btn.grid(row=2, column=0, pady=20)
        
    def log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_server_thread(self):
        self.start_btn.configure(state="disabled")
        threading.Thread(target=self.run_server, daemon=True).start()

    def run_server(self):
        self.log("=== SERVER STARTING ===")
        cert_pem, priv_pem = generate_self_signed_cert()
        uni_priv_rsa, uni_pub_rsa = generate_rsa_keypair()
        
        transcript_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'transcript.txt')
        if not os.path.exists(transcript_path):
            self.log("Error: transcript.txt not found. Run generate_mock_data.py")
            self.start_btn.configure(state="normal")
            return
            
        with open(transcript_path, 'rb') as f:
            transcript_data = f.read()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            self.log(f"Listening on {HOST}:{PORT}... Waiting for student connection.")
            conn, addr = s.accept()
            with conn:
                self.log(f"\n[+] Connected by {addr}")
                
                kerberos_passed = conn.recv(1024)
                if kerberos_passed == b"KERBEROS_OK":
                    self.log("[Phase 4] Kerberos Auth OK: STUDENT_987654321")
                
                self.log("\n[Phase 2] Initiating DH Exchange...")
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
                
                shared_secret = uni_dh.generate_shared_secret(student_pub_key)
                self.log(f"Shared Secret derived (hex): {shared_secret.hex()[:16]}...")
                
                conn.sendall(uni_pub_rsa)
                
                transcript_hash = compute_sha256(transcript_data)
                signature = sign_data(uni_priv_rsa, transcript_hash.encode())
                
                self.log(f"\n[Phase 1] Encrypting Transcript with AES...")
                aes_key = shared_secret[:16] 
                iv, ciphertext = encrypt_aes_cbc(aes_key, transcript_data)
                
                payload = {
                    'iv': iv.hex(),
                    'ciphertext': ciphertext.hex(),
                    'signature': signature.hex(),
                    'original_hash': transcript_hash
                }
                
                self.log("Sending Encrypted Package to Student...")
                conn.sendall(json.dumps(payload).encode())
                self.log("\n=== TRANSMISSION COMPLETE ===")
                self.start_btn.configure(state="normal")

if __name__ == "__main__":
    app = ServerGUI()
    app.mainloop()
