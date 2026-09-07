# Secure Academic Transcript Exchange System

A complete Python project simulating a University securely delivering a student's transcript through four security phases.

## Setup

1. Run the setup script for your OS:
   - Windows: `setup.bat`
   - Linux/Mac: `./setup.sh`
2. **IMPORTANT**: Activate the virtual environment before running any code.
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

## Usage (Graphical Interface - Recommended)

We have built a modern graphical interface to visually demonstrate the cryptography concepts.

**Phase 1: Cryptography Dashboard**
To test basic file encryption (AES vs 3-DES) and visually demonstrate ECB vs CBC image pattern leakage side-by-side:
```bash
python pipeline/gui_phase1.py
```

**Phase 5: Secure Client/Server TCP Exchange**
To simulate the secure transcript delivery over a network with Diffie-Hellman Key Exchange and Digital Signatures:
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
