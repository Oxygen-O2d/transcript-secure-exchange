from playwright.sync_api import sync_playwright
import time
import os
import base64

# Generate dummy files for the demo if they don't exist
DUMMY_TXT_PATH = os.path.join(os.path.dirname(__file__), "dummy.txt")
DUMMY_IMG_PATH = os.path.join(os.path.dirname(__file__), "dummy.png")

if not os.path.exists(DUMMY_TXT_PATH):
    with open(DUMMY_TXT_PATH, "w") as f:
        f.write("This is a dummy transcript file for benchmarking AES and 3-DES encryption speeds.")

if not os.path.exists(DUMMY_IMG_PATH):
    # 1x1 black pixel PNG base64
    b64_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
    with open(DUMMY_IMG_PATH, "wb") as f:
        f.write(base64.b64decode(b64_png))

def run_automated_demo():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html"))
    file_uri = f"file:///{frontend_path.replace(chr(92), '/')}"

    print("Launching Playwright Automated Demo...")
    
    with sync_playwright() as p:
        # Launch browser in visible mode (headless=False)
        # slow_mo=700 adds a 700ms delay between every action so the audience can see what's happening
        browser = p.chromium.launch(headless=False, slow_mo=700)
        page = browser.new_page()
        
        # Open the local HTML file
        page.goto(file_uri)
        
        print("Waiting for Cyber Gate animation to finish...")
        time.sleep(3) 

        # -------- PHASE 1 --------
        print("Navigating to Phase 1...")
        page.click("text=> Phase 1: Symmetric")
        
        print("Running AES vs 3-DES Benchmark...")
        page.set_input_files("input#p1-file", DUMMY_TXT_PATH)
        page.click("button:has-text('Run Benchmark')")
        page.wait_for_selector("#p1-bench-res span")
        time.sleep(2) # Pause for audience
        
        print("Running ECB vs CBC Image Pattern test...")
        page.set_input_files("input#p1-image", DUMMY_IMG_PATH)
        page.click("button:has-text('Test Pattern Leakage')")
        time.sleep(2)

        print("Running Avalanche Effect Analysis...")
        page.fill("input#p1-av-text", "Changing one bit changes everything")
        page.click("button:has-text('Analyze Bit Flips')")
        time.sleep(2)

        # -------- PHASE 2 --------
        print("Navigating to Phase 2...")
        page.click("text=> Phase 2: Asymmetric")
        
        print("Simulating RSA Hybrid Exchange...")
        page.click("button:has-text('Simulate Hybrid Exchange')")
        time.sleep(4) # Wait for logs to print
        
        print("Simulating Diffie-Hellman & MITM...")
        page.click("button:has-text('Simulate DH & MITM')")
        time.sleep(4)

        # -------- PHASE 3 --------
        print("Navigating to Phase 3...")
        page.click("text=> Phase 3: Integrity")
        
        print("Computing SHA-256 Hash...")
        page.fill("textarea#p3-hash-input", "Final Grade: A")
        page.click("button:has-text('Compute Hash')")
        time.sleep(2)
        
        print("Simulating Tampering...")
        page.fill("input#p3-tamp-text", "Final Grade: F")
        page.fill("input#p3-tamp-idx", "13") # Tamper with the 'F'
        page.click("button:has-text('Simulate Tampering')")
        time.sleep(3)

        # -------- PHASE 4 --------
        print("Navigating to Phase 4...")
        page.click("text=> Phase 4: Authentication")
        
        print("Generating Digital Signature...")
        page.click("button:has-text('Generate & Verify')")
        time.sleep(2)
        
        print("Generating X.509 Certificate...")
        page.click("button:has-text('Generate Mock Certificate')")
        time.sleep(2)
        
        print("Simulating Kerberos...")
        page.click("button:has-text('Step-by-Step Simulation')")
        time.sleep(5) # Wait for all 6 steps

        # -------- PHASE 5 --------
        print("Navigating to Phase 5...")
        page.click("text=> Phase 5: Pipeline")
        
        print("Starting Full Transmission Simulation...")
        page.click("button#btn-pipeline")
        
        # Wait for the WebSocket simulation to finish
        print("Watching the End-to-End Pipeline...")
        time.sleep(12) 
        
        print("Demo completed successfully! Closing in 3 seconds...")
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    run_automated_demo()
