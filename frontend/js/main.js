const API_URL = "http://127.0.0.1:8000/api";

// ----------------- THEME & ROUTING -----------------
const currentTheme = localStorage.getItem('ciphernet-theme') || 'dark';
if (currentTheme === 'light') {
    document.getElementById('theme-toggle').checked = true;
    document.body.classList.add('light-mode');
}

function toggleTheme(e) {
    if (e.checked) {
        document.body.classList.add('light-mode');
        localStorage.setItem('ciphernet-theme', 'light');
    } else {
        document.body.classList.remove('light-mode');
        localStorage.setItem('ciphernet-theme', 'dark');
    }
}

function nav(pageId, navElement) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(el => el.classList.remove('active'));
    // Show selected page
    document.getElementById(pageId).classList.add('active');
    
    // Update sidebar active state
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    if(navElement) navElement.classList.add('active');
    else {
        // If navigated programmatically, find the matching nav item
        const items = document.querySelectorAll('.nav-item');
        for(let item of items) {
            if(item.getAttribute('onclick').includes(`'${pageId}'`)) {
                item.classList.add('active');
                break;
            }
        }
    }
    
    // Update top title
    const titleMap = {
        'home': 'SYSTEM TERMINAL // DASHBOARD',
        'phase1': 'SECURITY LAB // SYMMETRIC ENCRYPTION',
        'phase2': 'SECURITY LAB // ASYMMETRIC KEY EXCHANGE',
        'phase3': 'SECURITY LAB // INTEGRITY VERIFICATION',
        'phase4': 'SECURITY LAB // AUTHENTICATION',
        'phase5': 'PIPELINE // SECURE TRANSMISSION',
        'attack': 'SECURITY ANALYSIS // ATTACK LAB',
        'packet': 'SECURITY ANALYSIS // PACKET ANALYSIS',
        'compare': 'SECURITY ANALYSIS // ALGORITHMS'
    };
    document.getElementById('top-title').innerText = titleMap[pageId] || 'SYSTEM TERMINAL';
}

function logToSystem(msg, type='info') {
    const sysLog = document.getElementById('sys-log');
    if(!sysLog) return;
    const color = type === 'error' ? 'var(--danger)' : (type === 'success' ? 'var(--success)' : 'var(--primary-cyan)');
    sysLog.innerHTML += `<p style="color:${color}">> ${msg}</p>`;
    sysLog.scrollTop = sysLog.scrollHeight;
}

// ----------------- PHASE 1 -----------------
function updateFileInfo() {
    const file = document.getElementById('p1-file').files[0];
    if(file) {
        document.getElementById('file-name').innerText = file.name;
        document.getElementById('file-size').innerText = `(${(file.size / 1024).toFixed(2)} KB)`;
    }
}

async function runBenchmark() {
    const fileInput = document.getElementById('p1-file');
    if (!fileInput.files[0]) return alert("Please upload a document first.");
    
    document.getElementById('res-aes').innerHTML = '<span class="text-cyan">measuring...</span>';
    document.getElementById('res-des').innerHTML = '<span class="text-cyan">measuring...</span>';
    logToSystem("Running AES vs 3-DES benchmark...");
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const res = await fetch(`${API_URL}/encrypt/file`, { method: 'POST', body: formData });
    const data = await res.json();
    
    document.getElementById('res-aes').innerHTML = `<span class="text-success">${data.aes_time}s</span>`;
    document.getElementById('res-des').innerHTML = `<span class="text-warning">${data.des_time}s</span>`;
    logToSystem(`Benchmark complete. AES: ${data.aes_time}s`, 'success');
}

async function runAvalanche() {
    const origText = document.getElementById('av-original').value;
    const modText = document.getElementById('av-modified').value;
    
    document.getElementById('av-ct1').innerText = "calculating...";
    document.getElementById('av-ct2').innerText = "calculating...";
    logToSystem("Analyzing Avalanche Effect bit differences...");
    
    // We only need to send the original text, the backend flips 1 bit.
    // The modText is just visual for the user in this simplified implementation.
    const res = await fetch(`${API_URL}/phase1/avalanche`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({plaintext: origText})
    });
    const data = await res.json();
    
    // Simulate ciphertext visuals
    document.getElementById('av-ct1').innerText = "A8 3F 91 C4 72 ... (Simulated output block)";
    document.getElementById('av-ct2').innerText = "D1 7A 34 B9 F1 ... (Simulated output block)";
    
    document.getElementById('av-diff-text').innerText = `${data.pt_diff_percent}%`;
    document.getElementById('av-progress').style.width = `${data.pt_diff_percent}%`;
    logToSystem(`Avalanche effect: ${data.pt_diff_percent}% bits changed`, 'success');
}

async function encryptImage() {
    const fileInput = document.getElementById('p1-image');
    if (!fileInput.files[0]) return;
    
    logToSystem("Running ECB vs CBC visual pattern leakage test...");
    
    // Show original
    const origUrl = URL.createObjectURL(fileInput.files[0]);
    document.getElementById('img-orig-container').innerHTML = `<img src="${origUrl}" style="max-height:100%;">`;
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const res = await fetch(`${API_URL}/encrypt/image`, { method: 'POST', body: formData });
    const data = await res.json();
    
    document.getElementById('img-ecb').src = data.ecb;
    document.getElementById('img-cbc').src = data.cbc;
    document.getElementById('img-ecb').style.display = 'block';
    document.getElementById('img-cbc').style.display = 'block';
    document.getElementById('lbl-ecb').style.display = 'block';
    document.getElementById('lbl-cbc').style.display = 'block';
    logToSystem("ECB Pattern Leakage demonstrated", 'error');
}

// ----------------- PHASE 2 -----------------
async function simHybrid() {
    logToSystem("Generating RSA Keypair and AES Session Key...");
    document.getElementById('hy-res').innerHTML = "";
    document.getElementById('hy-aes').innerText = "AES Key: generating...";
    const res = await fetch(`${API_URL}/phase2/rsa-hybrid`);
    const data = await res.json();
    
    setTimeout(() => {
        document.getElementById('hy-aes').innerHTML = `AES Key: <span class="text-cyan">${data.original_key}</span>`;
        logToSystem("AES session key generated");
    }, 500);
    setTimeout(() => {
        document.getElementById('hy-enc').innerText = `RSA Encrypted: ${data.encrypted_key_preview}`;
        logToSystem("AES key encrypted with University RSA Public Key");
    }, 1000);
    setTimeout(() => {
        document.getElementById('hy-dec').innerHTML = `Recovered: <span class="text-cyan">${data.decrypted_key}</span>`;
        if(data.match) document.getElementById('hy-res').innerHTML = `<span class="text-success">✓ Session key protected and successfully transmitted!</span>`;
        logToSystem("Session key recovered by Student RSA Private Key", 'success');
    }, 1500);
}

async function simDH() {
    logToSystem("Initializing Diffie-Hellman Key Exchange...");
    document.getElementById('dh-a').innerText = "generating...";
    document.getElementById('dh-b').innerText = "generating...";
    document.getElementById('dh-res').innerHTML = "";
    
    const res = await fetch(`${API_URL}/api/phase2/dh-mitm`.replace('/api/api', '/api'));
    const data = await res.json();
    
    setTimeout(() => {
        document.getElementById('dh-a').innerText = data.alice_secret;
        document.getElementById('dh-b').innerText = data.bob_secret;
        if(data.match) document.getElementById('dh-res').innerHTML = `✓ SHARED SECRET MATCH`;
        logToSystem(`DH Shared Secret matched: ${data.alice_secret.substring(0,8)}...`, 'success');
    }, 800);
}

async function simMITM() {
    logToSystem("Simulating Diffie-Hellman MITM Attack...", 'warning');
    document.getElementById('mitm-a').innerText = "intercepting...";
    document.getElementById('mitm-b').innerText = "intercepting...";
    document.getElementById('mitm-res').innerHTML = "";
    
    const res = await fetch(`${API_URL}/api/phase2/dh-mitm`.replace('/api/api', '/api'));
    const data = await res.json();
    
    setTimeout(() => {
        document.getElementById('mitm-a').innerText = data.mitm_alice;
        document.getElementById('mitm-b').innerText = data.mitm_bob;
        document.getElementById('mitm-res').innerHTML = `⚠ MITM SUCCESSFUL: Attacker controls both sessions!`;
        logToSystem("MITM Attack Successful. Authentication required.", 'error');
    }, 1000);
}

// ----------------- PHASE 3 -----------------
async function generateHash() {
    const text = document.getElementById('p3-data').value;
    logToSystem("Computing SHA-256 hash of transcript...");
    const res = await fetch(`${API_URL}/phase3/hash`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data: text})
    });
    const data = await res.json();
    document.getElementById('p3-hash-res').innerText = data.hash;
    logToSystem("Hash computation complete");
}

async function tamperHash() {
    const text = document.getElementById('p3-tamp').value;
    logToSystem("Simulating data tampering on transcript...", 'warning');
    const res = await fetch(`${API_URL}/phase3/tamper`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data: text, tamper_index: 0})
    });
    const data = await res.json();
    
    document.getElementById('p3-tamp-res').innerText = data.tampered_hash;
    if(!data.match) {
        document.getElementById('p3-tamp-status').innerHTML = `<span class="text-danger">⚠ INTEGRITY CHECK FAILED: Document Tampered!</span>`;
        logToSystem("Integrity verification failed. Tampering detected.", 'error');
    }
}

// ----------------- PHASE 4 -----------------
async function genSig() {
    logToSystem("Generating RSA Digital Signature...");
    const text = "Transcript";
    const res = await fetch(`${API_URL}/phase4/sign`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({data: text})
    });
    const data = await res.json();
    document.getElementById('p4-sig-res').innerText = data.signature;
    document.getElementById('p4-sig-verify').innerHTML = data.valid ? '<span class="text-success">✓ Signature Valid</span><br><span class="text-success">✓ University Identity Verified</span>' : '<span class="text-danger">✕ Invalid</span>';
    logToSystem("Signature generated and verified successfully", 'success');
}

async function genCert() {
    logToSystem("Generating X.509 Digital Certificate...");
    const res = await fetch(`${API_URL}/phase4/cert`);
    const data = await res.json();
    document.getElementById('p4-cert-res').style.display = "flex";
    document.getElementById('c-sub').innerText = data.subject;
    document.getElementById('c-iss').innerText = data.issuer;
    document.getElementById('c-pem').value = data.pem;
    logToSystem("X.509 Certificate loaded");
}

function simKerb() {
    const steps = [
        "1. Student requests TGT from Auth Server.",
        "2. Auth Server issues encrypted TGT.",
        "3. Student sends TGT to Ticket Granting Server.",
        "4. TGS issues Transcript Service Ticket.",
        "5. Student presents Ticket to University Server.",
        "6. Access GRANTED."
    ];
    const res = document.getElementById('kerb-steps');
    res.innerHTML = "";
    logToSystem("Starting Kerberos flow simulation...");
    steps.forEach((s, i) => {
        setTimeout(() => { 
            res.innerHTML += `<div style="padding:8px; border-left:2px solid var(--primary-cyan); margin-bottom:5px; background:var(--card-bg);">${s}</div>`; 
            logToSystem(`Kerberos: ${s}`);
            if(i === 5) logToSystem("Kerberos Authentication Complete", "success");
        }, i * 600);
    });
}

// ----------------- PHASE 5: PIPELINE -----------------
let ws = null;
function startPipeline() {
    document.getElementById('btn-pipeline').disabled = true;
    logToSystem("\n=== STARTING SECURE EXCHANGE PIPELINE ===");
    
    // Reset Flow Nodes
    const nodes = ['n-doc', 'n-aes', 'n-rsa', 'n-hash', 'n-sign', 'n-transmit', 'n-vsign', 'n-vhash', 'n-dec'];
    nodes.forEach(n => { document.getElementById(n).style.borderColor = 'var(--primary-cyan)'; document.getElementById(n).style.color = ''; });
    
    function highlightNode(id) {
        document.getElementById(id).style.borderColor = 'var(--success)';
        document.getElementById(id).style.color = 'var(--success)';
    }

    const sConsole = document.getElementById('p5-server-console');
    const cConsole = document.getElementById('p5-client-console');
    sConsole.innerHTML = "<p>> Initializing Secure Connection...</p>";
    cConsole.innerHTML = "<p>> Waiting for connection...</p>";
    
    if (ws) ws.close();
    ws = new WebSocket("ws://127.0.0.1:8000/ws/simulate");
    
    ws.onmessage = function(event) {
        const data = JSON.parse(event.data);
        const msg = data.message;
        
        if (data.role === 'server') {
            sConsole.innerHTML += `<p style="color:var(--success)">> ${msg}</p>`;
            sConsole.scrollTop = sConsole.scrollHeight;
        } else {
            cConsole.innerHTML += `<p style="color:var(--primary-cyan)">> ${msg}</p>`;
            cConsole.scrollTop = cConsole.scrollHeight;
        }
        
        // Map backend socket messages to frontend visual steps
        if(msg.includes("Kerberos Auth OK")) {
            highlightNode('n-doc');
        }
        else if(msg.includes("Initiating DH Exchange") || msg.includes("Generating RSA keypair")) {
            highlightNode('n-rsa');
        }
        else if(msg.includes("Shared Secret derived")) {
            // RSA Key Exchange Complete
        }
        else if(msg.includes("Encrypting Transcript")) {
            highlightNode('n-hash');
            highlightNode('n-sign');
            highlightNode('n-aes');
        }
        else if(msg.includes("Sending Encrypted Package")) {
            highlightNode('n-transmit');
            logToSystem("Transmitting packet over secure channel...", 'warning');
        }
        else if(msg.includes("Decrypting Transcript")) {
            highlightNode('n-dec');
        }
        else if(msg.includes("Integrity PASSED")) {
            highlightNode('n-vhash');
        }
        else if(msg.includes("Signature PASSED")) {
            highlightNode('n-vsign');
        }
        else if(msg.includes("TRANSMISSION COMPLETE")) {
            logToSystem("=== SECURE EXCHANGE SUCCESSFUL ===", 'success');
        }
    };
    
    ws.onclose = function() {
        document.getElementById('btn-pipeline').disabled = false;
        sConsole.innerHTML += `<br><p style="color:var(--warning)">> === CONNECTION CLOSED ===</p>`;
        cConsole.innerHTML += `<br><p style="color:var(--warning)">> === CONNECTION CLOSED ===</p>`;
    };
}
