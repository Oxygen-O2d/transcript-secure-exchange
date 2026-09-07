import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from phase3_integrity.hashing import compute_sha256, verify_hash

def simulate_tampering():
    print("[Phase 3 - Tamper Detection]")
    original_data = b"This is the genuine transcript data."
    expected_hash = compute_sha256(original_data)
    print(f"Original hash: {expected_hash}")
    
    tampered_data = bytearray(original_data)
    tampered_data[10] ^= 0xFF
    tampered_data = bytes(tampered_data)
    
    tampered_hash = compute_sha256(tampered_data)
    print(f"Tampered hash: {tampered_hash}")
    
    if not verify_hash(tampered_data, expected_hash):
        print("ALERT: Tampering detected! Hashes do not match.")
    else:
        print("Hash verified successfully.")

if __name__ == "__main__":
    simulate_tampering()
