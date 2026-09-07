## Cryptographic Algorithm Comparison

| Algorithm | Key Size | Speed (1MB Enc) | Speed (1MB Dec) | Known Attacks | Typical Real-World Use |
|-----------|----------|-----------------|-----------------|---------------|------------------------|
| AES-128 CBC | 128-bit | 0.0021s | 0.0018s | None practical on AES itself. Padding oracle if IV reused/improperly authenticated. | Standard for bulk data encryption (TLS, Disk encryption) |
| 3-DES CBC | 168-bit | 0.0355s | 0.0345s | Sweet32 (block collision due to 64-bit block size). | Legacy systems, old payment terminals, deprecated by NIST. |
| RSA-OAEP | 2048-bit | N/A (too slow) | N/A (too slow) | Factoring large primes (Shor's algorithm for quantum). Padding attacks if old PKCS#1 v1.5 used. | Key exchange, Digital Signatures (TLS handshake) |
