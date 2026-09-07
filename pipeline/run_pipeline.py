import subprocess
import sys
import time
import os

def run_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server_script = os.path.join(base_dir, 'pipeline', 'university_server.py')
    client_script = os.path.join(base_dir, 'pipeline', 'student_client.py')
    
    args = []
    if '--tamper' in sys.argv:
        args.append('--tamper')
    if '--mitm' in sys.argv:
        args.append('--mitm')
        
    print(f"Starting pipeline with args: {args}")
    
    server_process = subprocess.Popen([sys.executable, server_script] + args)
    time.sleep(1) # wait for server to bind
    
    client_process = subprocess.Popen([sys.executable, client_script])
    
    server_process.wait()
    client_process.wait()
    
    print("Pipeline execution completed.")

if __name__ == "__main__":
    run_pipeline()
