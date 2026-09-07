import hashlib

def compute_sha256(data):
    if isinstance(data, str):
        data = data.encode()
    digest = hashlib.sha256(data).hexdigest()
    return digest

def verify_hash(data, expected_hash):
    return compute_sha256(data) == expected_hash

if __name__ == "__main__":
    print("[Phase 3 - Hashing]")
    sample_data = b"Transcript Data for hashing test."
    h1 = compute_sha256(sample_data)
    print(f"Data hash (hex): {h1}")
    is_valid = verify_hash(sample_data, h1)
    print(f"Verification successful: {is_valid}")
