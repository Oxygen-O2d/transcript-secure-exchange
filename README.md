# Secure Academic Transcript Exchange System

A comprehensive Python project simulating a University securely delivering a student's transcript by guiding you through all core pillars of cryptography: Symmetric Encryption, Asymmetric Key Exchange, Integrity, and Authentication (PKI/Kerberos).

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
