import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt_image_ecb(image_path, out_path, key):
    with open(image_path, 'rb') as f:
        header = f.read(54) # BMP header is usually 54 bytes
        data = f.read()
    
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    with open(out_path, 'wb') as f:
        f.write(header)
        # To make it a valid BMP, we keep it the exact same length as original data portion
        f.write(encrypted_data[:len(data)])

def encrypt_image_cbc(image_path, out_path, key, iv):
    with open(image_path, 'rb') as f:
        header = f.read(54)
        data = f.read()
    
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    encrypted_data = cipher.encrypt(pad(data, AES.block_size))
    
    with open(out_path, 'wb') as f:
        f.write(header)
        f.write(encrypted_data[:len(data)])

if __name__ == "__main__":
    key = os.urandom(16)
    iv = os.urandom(16)
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    in_img = os.path.join(base_dir, 'data', 'sample_image.bmp')
    out_ecb = os.path.join(base_dir, 'data', 'encrypted_ecb.bmp')
    out_cbc = os.path.join(base_dir, 'data', 'encrypted_cbc.bmp')
    
    if not os.path.exists(in_img):
        print("Please run data/generate_mock_data.py first.")
        exit(1)
        
    encrypt_image_ecb(in_img, out_ecb, key)
    encrypt_image_cbc(in_img, out_cbc, key, iv)
    print(f"[Phase 1 - ECB vs CBC] Encrypted images saved to data/encrypted_ecb.bmp and data/encrypted_cbc.bmp")
