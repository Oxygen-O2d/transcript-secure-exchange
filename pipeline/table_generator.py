import os
import csv

def generate_table():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    csv_path = os.path.join(base_dir, 'data', 'benchmark_results.csv')
    md_path = os.path.join(base_dir, 'data', 'comparative_table.md')
    
    if not os.path.exists(csv_path):
        print("Run phase1_symmetric/benchmark.py first.")
        return
        
    markdown = "## Cryptographic Algorithm Comparison\n\n"
    markdown += "| Algorithm | Key Size | Speed (1MB Enc) | Speed (1MB Dec) | Known Attacks | Typical Real-World Use |\n"
    markdown += "|-----------|----------|-----------------|-----------------|---------------|------------------------|\n"
    
    aes_enc_1mb = "N/A"
    aes_dec_1mb = "N/A"
    des3_enc_1mb = "N/A"
    des3_dec_1mb = "N/A"
    
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Size'] == '1mb':
                aes_enc_1mb = f"{float(row['AES_Enc']):.4f}s"
                aes_dec_1mb = f"{float(row['AES_Dec']):.4f}s"
                des3_enc_1mb = f"{float(row['3DES_Enc']):.4f}s"
                des3_dec_1mb = f"{float(row['3DES_Dec']):.4f}s"
                
    markdown += f"| AES-128 CBC | 128-bit | {aes_enc_1mb} | {aes_dec_1mb} | None practical on AES itself. Padding oracle if IV reused/improperly authenticated. | Standard for bulk data encryption (TLS, Disk encryption) |\n"
    markdown += f"| 3-DES CBC | 168-bit | {des3_enc_1mb} | {des3_dec_1mb} | Sweet32 (block collision due to 64-bit block size). | Legacy systems, old payment terminals, deprecated by NIST. |\n"
    markdown += "| RSA-OAEP | 2048-bit | N/A (too slow) | N/A (too slow) | Factoring large primes (Shor's algorithm for quantum). Padding attacks if old PKCS#1 v1.5 used. | Key exchange, Digital Signatures (TLS handshake) |\n"
    
    with open(md_path, 'w') as f:
        f.write(markdown)
    
    print(f"Generated comparative table at data/comparative_table.md")
    print(markdown)

if __name__ == "__main__":
    generate_table()
