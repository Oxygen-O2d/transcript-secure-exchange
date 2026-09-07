import requests
import os
import base64

def generate_diagram():
    diagram = """
sequenceDiagram
    participant S as Student Client
    participant K as Kerberos AS/TGS
    participant U as University Server
    
    S->>K: 1. Request TGT
    K-->>S: 2. Verify & Issue TGT
    S->>K: 3. Request Service Ticket
    K-->>S: 4. Issue Service Ticket for Transcript
    S->>U: 5. Present Service Ticket
    U-->>S: 6. Access Granted
    
    note over S,U: Phase 2 - Key Exchange
    U->>S: 7. Diffie-Hellman Params + Uni Public Key
    S->>U: 8. Student Public Key
    note over S,U: Shared Secret Derived (AES Key)
    
    note over U: Phase 3 & 4
    U->>U: 9. Compute SHA-256 of Transcript
    U->>U: 10. Sign Hash with RSA Private Key
    U->>U: 11. Encrypt Transcript with AES-CBC
    
    U->>S: 12. Send Encrypted Package
    
    note over S: Decryption & Verification
    S->>S: 13. Decrypt with AES Key
    S->>S: 14. Verify Hash (Integrity)
    S->>S: 15. Verify Signature with Uni RSA Pub Key
    """
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    mmd_path = os.path.join(base_dir, 'pipeline', 'architecture.mmd')
    png_path = os.path.join(base_dir, 'report', 'architecture.png')
    
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    
    with open(mmd_path, 'w') as f:
        f.write(diagram)
        
    print("Saved architecture.mmd")
    
    try:
        graphbytes = diagram.encode("utf8")
        base64_bytes = base64.b64encode(graphbytes)
        base64_string = base64_bytes.decode("ascii")
        
        url = f"https://mermaid.ink/img/{base64_string}"
        response = requests.get(url)
        if response.status_code == 200:
            with open(png_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded architecture.png to {png_path}")
        else:
            print(f"Failed to download image: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Failed to generate diagram PNG: {e}")

if __name__ == "__main__":
    generate_diagram()
