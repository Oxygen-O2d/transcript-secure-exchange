import customtkinter as ctk
import socket
import threading
import sys
import os
import json
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import decrypt_aes_cbc
from phase2_asymmetric.dh_exchange import DHParticipant
from phase3_integrity.hashing import compute_sha256
from phase4_authentication.digital_signature import verify_signature

HOST = '127.0.0.1'
PORT = 65432

class ClientGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Student Client (Receiver)")
        self.geometry("600x500")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        self.header = ctk.CTkLabel(self, text="Student Transcript Portal", font=("Arial", 20, "bold"))
        self.header.grid(row=0, column=0, pady=10)
        
        self.log_box = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 12))
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.req_btn = ctk.CTkButton(self, text="Request Transcript securely", command=self.start_client_thread)
        self.req_btn.grid(row=2, column=0, pady=20)
        
    def log(self, text):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def start_client_thread(self):
        self.req_btn.configure(state="disabled")
        threading.Thread(target=self.run_client, daemon=True).start()

    def run_client(self):
        self.log("=== CLIENT STARTING ===")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                self.log("[+] Connected to University Server.")
                
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
                self.log(f"Shared Secret derived (hex): {shared_secret.hex()[:16]}...")
                
                uni_pub_rsa = s.recv(1024)
                
                payload_bytes = s.recv(4096)
                payload = json.loads(payload_bytes.decode())
                
                iv = bytes.fromhex(payload['iv'])
                ciphertext = bytes.fromhex(payload['ciphertext'])
                signature = bytes.fromhex(payload['signature'])
                expected_hash = payload['original_hash']
                
                self.log("\n[Phase 1] Decrypting Transcript...")
                aes_key = shared_secret[:16]
                plaintext = decrypt_aes_cbc(aes_key, iv, ciphertext)
                
                preview = plaintext[:40].decode(errors='ignore').replace('\n', ' ')
                self.log(f"Decrypted Preview: {preview}...")
                    
                self.log("\n[Phase 3] Verifying Integrity...")
                current_hash = compute_sha256(plaintext)
                if current_hash == expected_hash:
                    self.log(f"-> Integrity PASSED! Hash matches.")
                else:
                    self.log(f"-> Integrity FAILED!")
                    
                self.log("\n[Phase 4] Verifying Signature...")
                is_valid_sig = verify_signature(uni_pub_rsa, expected_hash.encode(), signature)
                if is_valid_sig:
                    self.log("-> Signature PASSED! Authentic Sender.")
                else:
                    self.log("-> Signature FAILED!")
                    
                self.log("\n=== TRANSCRIPT RECEIVED SUCCESSFULLY ===")
        except ConnectionRefusedError:
            self.log("\nError: Could not connect to the server. Is the University Server running?")
        except Exception as e:
            self.log(f"\nError occurred: {e}")
        finally:
            self.req_btn.configure(state="normal")

if __name__ == "__main__":
    app = ClientGUI()
    app.mainloop()
