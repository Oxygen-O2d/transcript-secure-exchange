# Cryptographic Algorithms Explained

This document provides a detailed explanation of the cryptographic algorithms implemented in the Secure Academic Transcript Exchange System.

## 1. Symmetric Encryption Algorithms

Symmetric encryption uses the same key for both encryption and decryption. It is typically very fast and used for bulk data encryption.

### AES (Advanced Encryption Standard)
- **What it is:** A symmetric block cipher adopted by the U.S. government as the standard encryption algorithm. In this project, we used AES-128 (meaning the secret key is 128 bits long).
- **How it works:** It processes data in fixed 128-bit blocks, applying multiple rounds (10 rounds for a 128-bit key) of substitution, permutation, and mixing operations to scramble the plaintext.
- **Why we used it:** AES is the current industry standard for securing data at rest and in transit. It is fast, highly secure against modern cryptanalysis, and computationally efficient.

### 3-DES (Triple Data Encryption Algorithm)
- **What it is:** A legacy symmetric block cipher that applies the original DES cipher algorithm three times to each data block.
- **How it works:** It uses a 168-bit key (conceptually three 56-bit keys) and processes data in 64-bit blocks. The process is Encrypt-Decrypt-Encrypt (EDE).
- **Why we used it:** We implemented 3-DES strictly as a benchmark comparison against AES. It is significantly slower and less secure due to its small block size (susceptible to the Sweet32 collision attack) and is being officially deprecated by NIST.

### Modes of Operation: ECB vs. CBC
Block ciphers require a "mode of operation" to encrypt data larger than a single block.
- **ECB (Electronic Codebook):** The simplest mode where each block of plaintext is encrypted independently. **Flaw:** Identical plaintext blocks produce identical ciphertext blocks, meaning structural patterns in the original data (like an image) remain visible.
- **CBC (Cipher Block Chaining):** A secure mode where each block of plaintext is XORed with the previous ciphertext block before being encrypted. An Initialization Vector (IV) is used for the very first block. **Advantage:** Identical plaintext blocks encrypt to entirely different ciphertext blocks, completely hiding data patterns.

---

## 2. Asymmetric Encryption & Key Exchange

Asymmetric encryption uses a mathematically linked key pair: a public key (can be shared openly) and a private key (kept secret). 

### Diffie-Hellman (DH) Key Exchange
- **What it is:** A method for two parties to securely establish a shared secret over an insecure, public channel.
- **How it works:** It relies on the mathematical difficulty of computing discrete logarithms. Both parties generate their own private/public components. They exchange public components and combine them with their own private components. The mathematics ensure both arrive at the exact same shared secret.
- **Why we used it:** To allow the University and Student to agree on an AES session key without ever sending the key itself across the network.
- **Vulnerability (MITM):** Standard DH does not authenticate the parties, making it vulnerable to Man-in-the-Middle attacks where an attacker intercepts the exchange and establishes separate keys with both parties.

### HKDF (HMAC-based Key Derivation Function)
- **What it is:** A function that takes a raw, potentially weak, or irregularly sized secret (like the raw mathematical output of Diffie-Hellman) and derives a strong, uniform cryptographic key of a specific length.
- **Why we used it:** To safely convert the Diffie-Hellman shared secret into a clean 128-bit key suitable for AES.

### RSA (Rivest–Shamir–Adleman)
- **What it is:** One of the oldest and most widely used public-key cryptosystems, relying on the practical difficulty of factoring the product of two very large prime numbers. We used 2048-bit keys.
- **How it works (Encryption):** Data encrypted with the public key can only be decrypted by the corresponding private key. 
- **Padding (OAEP):** We used RSA-OAEP (Optimal Asymmetric Encryption Padding) which adds randomness to the plaintext before encryption, preventing deterministic attacks.
- **Why we used it:** RSA is too slow for bulk data (like an entire transcript file). Instead, we used it for **Hybrid Encryption**: securely encrypting the small AES session key and sending it to the recipient.

---

## 3. Data Integrity & Hashing

### SHA-256 (Secure Hash Algorithm 2)
- **What it is:** A cryptographic hash function that takes an input of any size and produces a fixed-size 256-bit (32-byte) unique mathematical summary (digest) of that data.
- **How it works:** It is a one-way function—you cannot reverse the hash to get the original data. A tiny change in the input (even one bit) completely changes the resulting hash (the Avalanche effect).
- **Why we used it:** To provide data integrity. By computing the hash of the transcript before sending it, and comparing it to the hash of the decrypted transcript upon receipt, we can detect if the file was tampered with or corrupted in transit.

---

## 4. Authentication & Digital Signatures

### RSA Digital Signatures
- **What it is:** Reversing the standard RSA encryption process to prove identity and authenticity.
- **How it works:** Instead of encrypting the entire transcript, the University computes the SHA-256 hash of the transcript and "encrypts" (signs) that hash using their **Private Key**. 
- **Verification:** The Student decrypts the signature using the University's **Public Key** to reveal the hash, and checks if it matches their own computed hash of the transcript. If it matches, it proves the University sent it (Authentication) and the data wasn't altered (Integrity). 

### X.509 Certificates
- **What it is:** A standard format for public key certificates.
- **How it works:** It acts as a digital ID card. It securely binds a public key (like the University's RSA public key) to an identity (University Registrar), usually signed by a trusted Certificate Authority (CA). 
- **Why we used it:** In the real world, the Student needs a way to trust that the public key they are using actually belongs to the University and not an attacker. The X.509 certificate provides this verifiable identity binding.
