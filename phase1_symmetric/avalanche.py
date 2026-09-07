import os
import sys

# Ensure imports work when run as script or module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc

def flip_bit(data, byte_index, bit_index):
    mutable_data = bytearray(data)
    mutable_data[byte_index] ^= (1 << bit_index)
    return bytes(mutable_data)

def count_bit_differences(bytes1, bytes2):
    diff = 0
    for b1, b2 in zip(bytes1, bytes2):
        xor = b1 ^ b2
        diff += bin(xor).count('1')
    return diff

def demonstrate_avalanche():
    key = os.urandom(16)
    plaintext = b"This is a sample plaintext block to demonstrate the avalanche effect in AES."
    
    iv1, ciphertext1 = encrypt_aes_cbc(key, plaintext)
    
    # 1. Flip a bit in plaintext
    plaintext_altered = flip_bit(plaintext, 0, 0)
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    cipher_pt = AES.new(key, AES.MODE_CBC, iv=iv1)
    ciphertext2 = cipher_pt.encrypt(pad(plaintext_altered, AES.block_size))
    
    # 2. Flip a bit in key
    key_altered = flip_bit(key, 0, 0)
    cipher_key = AES.new(key_altered, AES.MODE_CBC, iv=iv1)
    ciphertext3 = cipher_key.encrypt(pad(plaintext, AES.block_size))
    
    total_bits = len(ciphertext1) * 8
    
    diff_pt = count_bit_differences(ciphertext1, ciphertext2)
    diff_key = count_bit_differences(ciphertext1, ciphertext3)
    
    print("[Phase 1 - Avalanche Effect]")
    print(f"Total bits in ciphertext: {total_bits}")
    print(f"Bit difference after 1 bit change in plaintext: {diff_pt} ({(diff_pt/total_bits)*100:.2f}%)")
    print(f"Bit difference after 1 bit change in key: {diff_key} ({(diff_key/total_bits)*100:.2f}%)")

if __name__ == "__main__":
    demonstrate_avalanche()
