from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os

def generate_rsa_keypair(bits=2048):
    key = RSA.generate(bits)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def rsa_encrypt_session_key(public_key_pem, session_key):
    recipient_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    return enc_session_key

def rsa_decrypt_session_key(private_key_pem, enc_session_key):
    private_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    session_key = cipher_rsa.decrypt(enc_session_key)
    return session_key

if __name__ == "__main__":
    print("[Phase 2 - RSA Hybrid Encryption]")
    priv, pub = generate_rsa_keypair()
    aes_session_key = os.urandom(16)
    print(f"Original AES session key (hex): {aes_session_key.hex()}")
    
    enc_key = rsa_encrypt_session_key(pub, aes_session_key)
    print(f"Encrypted session key (hex, truncated): {enc_key[:16].hex()}...")
    
    dec_key = rsa_decrypt_session_key(priv, enc_key)
    print(f"Decrypted AES session key (hex): {dec_key.hex()}")
    assert aes_session_key == dec_key
