from Crypto.Cipher import AES, DES3
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_aes_cbc(key, data):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))
    return cipher.iv, ciphertext

def decrypt_aes_cbc(key, iv, ciphertext):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext

def encrypt_3des_cbc(key, data):
    cipher = DES3.new(key, DES3.MODE_CBC)
    ciphertext = cipher.encrypt(pad(data, DES3.block_size))
    return cipher.iv, ciphertext

def decrypt_3des_cbc(key, iv, ciphertext):
    cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext), DES3.block_size)
    return plaintext

if __name__ == "__main__":
    print("Testing encryption algorithms...")
    test_data = b"Hello, Secure Transcript World!"
    aes_key = os.urandom(16)
    iv, ct = encrypt_aes_cbc(aes_key, test_data)
    pt = decrypt_aes_cbc(aes_key, iv, ct)
    assert pt == test_data
    print(f"[Phase 1 - AES] Encryption/Decryption successful. Ciphertext (hex, truncated): {ct[:16].hex()}...")

    des3_key = DES3.adjust_key_parity(os.urandom(24))
    iv3, ct3 = encrypt_3des_cbc(des3_key, test_data)
    pt3 = decrypt_3des_cbc(des3_key, iv3, ct3)
    assert pt3 == test_data
    print(f"[Phase 1 - 3DES] Encryption/Decryption successful. Ciphertext (hex, truncated): {ct3[:16].hex()}...")
