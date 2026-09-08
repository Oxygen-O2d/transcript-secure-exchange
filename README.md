# Secure Academic Transcript Exchange System

A complete Python project simulating a University securely delivering a student's transcript through four security phases.

## Setup

1. Run the setup script for your OS:
   - Windows: `setup.bat`
   - Linux/Mac: `./setup.sh`
2. **IMPORTANT**: Activate the virtual environment before running any code.
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

## Usage (Web Interface - New & Recommended)

We have built a modern Web-based dashboard to visually demonstrate the cryptography concepts.

### 1. Start the Backend API
The web dashboard relies on a Python FastAPI server to perform cryptographic operations.
1. Open a terminal and ensure your virtual environment is activated.
2. Start the server:
   ```bash
   python backend/app.py
   ```
   *The server will run at `http://127.0.0.1:8000`.*

### 2. Open the Frontend
1. Open your File Explorer.
2. Navigate to the `frontend` directory in this project.
3. Double-click on `index.html` to open the secure dashboard in your default web browser.

**Features Available in the Web Dashboard:**
- **Phase 1: Cryptography Dashboard:** Test file encryption and visually demonstrate ECB vs CBC image pattern leakage.
- **Phase 5: Secure Exchange Simulation:** Simulate transcript delivery with Diffie-Hellman and Digital Signatures via real-time WebSocket logs.

---

## Usage (Legacy Desktop GUI)

If you prefer to use the older Python `customtkinter` interface:

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

## Usage (Command Line Interface)

If you prefer to run the scripts headlessly, generate the mock data first:
```bash
python data/generate_mock_data.py
```

Run the full integration pipeline via the CLI orchestrator:
```bash
python pipeline/run_pipeline.py
```
