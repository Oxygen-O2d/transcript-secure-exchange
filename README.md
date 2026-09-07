# Secure Academic Transcript Exchange System

A complete Python project simulating a University securely delivering a student's transcript through four security phases.

## Setup

1. Run the setup script for your OS:
   - Windows: `setup.bat`
   - Linux/Mac: `./setup.sh`
2. **IMPORTANT**: Activate the virtual environment before running any code.
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

## Usage

Generate mock data first:
```bash
python data/generate_mock_data.py
```

Run individual phases or the full integration pipeline. The integration pipeline simulates communication over sockets.

```bash
# Run server
python pipeline/university_server.py
# In a separate terminal, run client
python pipeline/student_client.py
```
Or use the orchestrator:
```bash
python pipeline/run_pipeline.py
```
