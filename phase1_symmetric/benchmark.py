import time
import os
import csv
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase1_symmetric.encryption import encrypt_aes_cbc, encrypt_3des_cbc, decrypt_aes_cbc, decrypt_3des_cbc
from Crypto.Cipher import DES3

def benchmark():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sizes = ['10kb', '100kb', '1mb']
    
    results = []
    
    aes_key = os.urandom(16)
    des3_key = DES3.adjust_key_parity(os.urandom(24))
    
    print("[Phase 1 - Benchmarks]")
    for size in sizes:
        file_path = os.path.join(base_dir, 'data', f'test_{size}.txt')
        if not os.path.exists(file_path):
            print(f"Skipping {size}, run generate_mock_data.py first.")
            continue
            
        with open(file_path, 'rb') as f:
            data = f.read()
            
        # AES
        start = time.time()
        iv, ct = encrypt_aes_cbc(aes_key, data)
        aes_enc_time = time.time() - start
        
        start = time.time()
        decrypt_aes_cbc(aes_key, iv, ct)
        aes_dec_time = time.time() - start
        
        # 3DES
        start = time.time()
        iv3, ct3 = encrypt_3des_cbc(des3_key, data)
        des3_enc_time = time.time() - start
        
        start = time.time()
        decrypt_3des_cbc(des3_key, iv3, ct3)
        des3_dec_time = time.time() - start
        
        results.append({
            'Size': size,
            'AES_Enc': f"{aes_enc_time:.6f}",
            'AES_Dec': f"{aes_dec_time:.6f}",
            '3DES_Enc': f"{des3_enc_time:.6f}",
            '3DES_Dec': f"{des3_dec_time:.6f}"
        })
        
        print(f"  Size: {size}")
        print(f"    AES  Enc: {aes_enc_time:.6f}s | Dec: {aes_dec_time:.6f}s")
        print(f"    3DES Enc: {des3_enc_time:.6f}s | Dec: {des3_dec_time:.6f}s")

    csv_path = os.path.join(base_dir, 'data', 'benchmark_results.csv')
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['Size', 'AES_Enc', 'AES_Dec', '3DES_Enc', '3DES_Dec'])
        writer.writeheader()
        writer.writerows(results)
    print(f"Benchmark results saved to data/benchmark_results.csv")

if __name__ == "__main__":
    benchmark()
