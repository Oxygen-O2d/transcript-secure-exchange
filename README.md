# Secure Academic Transcript Exchange System

A comprehensive Python project simulating a University securely delivering a student's transcript by guiding you through all core pillars of cryptography: Symmetric Encryption, Asymmetric Key Exchange, Integrity, and Authentication (PKI/Kerberos).

## 📖 How This Works (A Guide for Non-IT Backgrounds)

Imagine a University trying to send a highly sensitive academic transcript to a student over the internet. You need to guarantee three things:
1. No one else can read it (**Confidentiality**).
2. No one can secretly change the grades while it is in transit (**Integrity**).
3. The student knows it genuinely came from the university, and the university knows they are sending it to the right student (**Authentication**).

This project demonstrates how modern digital security achieves this in **5 Phases**:

### Phase 1: Symmetric Cryptography (The Secret Key)
* **What it is:** The sender and receiver use the exact same "secret key" to lock and unlock the message.
* **Real-World Analogy:** You put the transcript in a locked box. Both you and the student have a copy of the exact same physical key to open it.
* **What we demonstrate:** We show how algorithms (like AES and 3-DES) mathematically scramble the data so it looks like gibberish to anyone else.

### Phase 2: Asymmetric Cryptography (The Public Padlock)
* **What it is:** Using the *same* key to lock and unlock is risky—how do you securely give the student the key in the first place? Asymmetric cryptography solves this by using a pair of keys: a **Public Key** (a padlock anyone can use to lock the box) and a **Private Key** (the only key that can unlock it).
* **Real-World Analogy:** The student sends you an open padlock. You put the transcript in the box, snap their padlock shut, and mail it back. Now, only the student can open it because they hold the only key to that padlock.
* **What we demonstrate:** We simulate this "padlock exchange" (Diffie-Hellman Key Exchange) and show how we can safely establish a secret connection even if a hacker is listening.

### Phase 3: Integrity (The Tamper-Evident Seal)
* **What it is:** How do we know the transcript wasn't altered (e.g., someone changing a 'C' grade to an 'A') while it was traveling? We use "Hashing" to create a unique digital fingerprint of the document.
* **Real-World Analogy:** You place a special wax seal on the envelope. If anyone tries to open the envelope and change the document, the seal breaks. When the student receives it, they check if the seal is intact.
* **What we demonstrate:** We show how generating a "Hash" works. We then simulate a hacker flipping a single bit of data (tampering) and show how the system instantly detects it because the fingerprint no longer matches.

### Phase 4: Authentication & PKI (The Notary Public & ID Card)
* **What it is:** How does the student know the transcript *actually* came from the University and not a scammer pretending to be the University? We use Digital Signatures and Digital Certificates.
* **Real-World Analogy:** The university signs the document in front of a Notary Public. The Notary stamps it to verify the university's identity. Furthermore, we use a system called Kerberos, which acts like a bouncer checking your ID card before letting you into a VIP room.
* **What we demonstrate:** We show how Digital Signatures are created and verified. We also generate mock "Digital Certificates" (like digital passports) and walk through a Kerberos login gate.

### Phase 5: Pipeline Simulation (Putting It All Together)
* **What it is:** Real-world systems don't use just one of these methods; they use all of them together!
* **Real-World Analogy:** The student shows their ID to the bouncer (Authentication). The student and university exchange open padlocks (Asymmetric). The university puts the transcript in a box, seals it with a tamper-evident seal (Integrity), locks it with a secret key (Symmetric), locks *that* secret key with the student's padlock, and sends it.
* **What we demonstrate:** A live, step-by-step simulation of a student requesting their transcript, and the university server securely packaging and delivering it using every security concept from Phases 1 through 4.

## 🚀 Setup

1. Run the setup script for your OS to create a Python virtual environment and install dependencies:
   - **Windows:** `setup.bat`
   - **Linux/Mac:** `./setup.sh`
   
2. **IMPORTANT**: Activate the virtual environment before running any code.
   - **Windows:** `venv\Scripts\activate`
   - **Linux/Mac:** `source venv/bin/activate`

---

## 🌐 Usage (Modern Web Interface - Recommended)

We have built a fully featured, modern Web-based dashboard to visually demonstrate all cryptography concepts across 5 phases.

### 1. Start the Backend API Server
The web dashboard relies on a Python FastAPI server to perform real cryptographic operations securely in the backend.

Open a terminal, activate your virtual environment, and start the server:
```bash
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```
*(The API server will run at `http://127.0.0.1:8000`. You can view the automated API documentation at `http://127.0.0.1:8000/docs`)*

### 2. Start the Frontend Server
Open a **second** terminal, activate your virtual environment, and serve the frontend files:
```bash
python -m http.server 8080 --directory frontend
```

### 3. Open the Dashboard
Navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080) in your web browser. 

**Features Available in the Web Dashboard:**
- **Phase 1: Symmetric Cryptography:** Benchmark AES vs 3-DES, demonstrate ECB vs CBC image pattern leakage, and test the AES Avalanche Effect.
- **Phase 2: Asymmetric Cryptography:** Simulate Diffie-Hellman Key Exchange (with Man-in-the-Middle visualization) and RSA Hybrid Encryption.
- **Phase 3: Integrity:** Compute SHA-256 hashes and interactively simulate Tamper Detection via bit-flipping.
- **Phase 4: Authentication & PKI:** Sign & verify data with RSA Digital Signatures, issue mock X.509 Certificates, and step through a Kerberos authentication gate.
- **Phase 5: Pipeline Simulation:** Watch a live, end-to-end WebSocket simulation of a student requesting and securely receiving their transcript from the University server.

---

## 🖥️ Usage (Legacy Desktop GUI)

If you prefer to use the older Python `customtkinter` desktop interface:

**Phase 1: Cryptography Dashboard**
```bash
python pipeline/gui_phase1.py
```

**Phase 5: Secure Client/Server TCP Exchange**
To simulate the secure transcript delivery over a network:
1. Open a terminal and start the University Server:
   ```bash
   python pipeline/gui_server.py
   ```
2. Open a *second* terminal and start the Student Client:
   ```bash
   python pipeline/gui_client.py
   ```

---

## 💻 Usage (Command Line Interface)

If you prefer to run the scripts headlessly, generate the mock data first:
```bash
python data/generate_mock_data.py
```

Run the full integration pipeline via the CLI orchestrator:
```bash
python pipeline/run_pipeline.py
```
