# CipherNet: Secure Exchange Execution Guide

This document outlines the exact workflow and commands required to execute the CipherNet application using the new HTML/JS/FastAPI architecture.

## 1. Environment Setup

First, ensure you are in the correct directory and your virtual environment is activated.

Open a PowerShell terminal and run:
```powershell
# Navigate to the project directory (if not already there)
cd "d:\Study\Sem 7\Information Security (3170720)\Cipat\transcript-secure-exchange"

# Activate the virtual environment
.\venv\Scripts\Activate.ps1

# Ensure all dependencies are installed
pip install -r requirements.txt
```

## 2. Start the Application

Because this is a decoupled architecture, you need to run the Backend and the Frontend separately.

### Step 2a: Start the FastAPI Backend
In your activated terminal, start the Python backend server:
```powershell
python backend/app.py
```
*(Leave this terminal open. It will say `Uvicorn running on http://127.0.0.1:8000`)*

### Step 2b: Open the Frontend
You do not need a special server for the frontend! Since it is pure HTML/CSS/JS, simply double click the `index.html` file to open it in Chrome or Edge:
```powershell
# Open a NEW terminal or just double-click the file in File Explorer
Start-Process "frontend\index.html"
```

## 3. Execution Workflow (Phase by Phase)

Once the browser opens, use the sidebar to navigate through the project phases.

### Phase 1: Symmetric
- **Benchmark:** Upload any text file and click "Run Benchmark" to see the speed difference between AES and 3-DES.
- **ECB vs CBC:** Upload a picture to visually see how ECB leaks image patterns while CBC completely randomizes them.
- **Avalanche Effect:** Type text and analyze to see the ~50% bit flip ratio when a single bit is changed.

### Phase 2: Asymmetric
- **Hybrid Exchange:** Click Simulate to watch the system use a slow RSA public key to securely exchange a fast AES session key.
- **MITM Simulation:** Click Simulate to watch Diffie-Hellman securely generate shared secrets, and then watch Eve intercept them in real-time.

### Phase 3: Integrity
- **Hashing:** Type any transcript data to generate its unique SHA-256 fingerprint.
- **Tamper Simulation:** Change the index slider to flip one character and prove that the receiver's hash will no longer match the sender's hash.

### Phase 4: Authentication
- **Digital Signatures:** Generate a cryptographic signature that proves the University sent the file.
- **Certificate:** Generate and view a mock X.509 PKI certificate.
- **Kerberos:** Step through the 6-step Ticket Granting process.

### Phase 5: Pipeline
- Navigate to Phase 5 and click the big **Start Full Transmission Simulation** button.
- Sit back and watch the live console as it automates the Kerberos Auth -> DH Key Exchange -> Transcript Hashing & Signing -> AES Encryption -> Transmission -> Decryption -> Hash & Signature Verification sequence!
