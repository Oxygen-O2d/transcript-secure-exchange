from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import os

def sign_data(private_key_pem, data):
    if isinstance(data, str):
        data = data.encode()
    key = RSA.import_key(private_key_pem)
    h = SHA256.new(data)
    signature = pkcs1_15.new(key).sign(h)
    return signature

def verify_signature(public_key_pem, data, signature):
    if isinstance(data, str):
        data = data.encode()
    key = RSA.import_key(public_key_pem)
    h = SHA256.new(data)
    try:
        pkcs1_15.new(key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False

if __name__ == "__main__":
    print("[Phase 4 - Digital Signature]")
    key = RSA.generate(2048)
    priv = key.export_key()
    pub = key.publickey().export_key()
    
    data = b"This transcript is verified and genuine."
    sig = sign_data(priv, data)
    print(f"Signature generated (hex, truncated): {sig[:16].hex()}...")
    
    is_valid = verify_signature(pub, data, sig)
    print(f"Signature valid: {is_valid}")
    
    is_valid_tampered = verify_signature(pub, b"This transcript is verified and fake.", sig)
    print(f"Signature valid on tampered data: {is_valid_tampered}")
