document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = 'http://127.0.0.1:8000';

    // Navigation
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.view-section');
    const pageTitle = document.getElementById('page-title');
    const pageDesc = document.getElementById('page-desc');

    const phaseTitles = {
        'phase1': { title: 'Phase 1: Symmetric Cryptography', desc: 'Test encryption algorithms, visualize cipher modes, and observe the avalanche effect.' },
        'phase2': { title: 'Phase 2: Asymmetric Cryptography', desc: 'Simulate Diffie-Hellman Key Exchanges, MITM attacks, and RSA Hybrid Encryption.' },
        'phase3': { title: 'Phase 3: Integrity & Tamper Detection', desc: 'Compute hashes and detect malicious modifications in transit.' },
        'phase4': { title: 'Phase 4: Authentication & PKI', desc: 'Verify identity via Digital Signatures, X.509 Certificates, and Kerberos.' },
        'phase5': { title: 'Phase 5: Pipeline Simulation', desc: 'Live end-to-end transcript exchange simulating all 4 phases together.' }
    };

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            const targetId = link.getAttribute('data-target');
            sections.forEach(sec => sec.classList.remove('active'));
            document.getElementById(targetId).classList.add('active');
            
            pageTitle.textContent = phaseTitles[targetId].title;
            pageDesc.textContent = phaseTitles[targetId].desc;
        });
    });

    const appendTerminal = (terminalId, text, color = '#38bdf8') => {
        const term = document.getElementById(terminalId);
        term.classList.remove('hidden');
        const line = document.createElement('div');
        line.className = 'log-line';
        line.style.color = color;
        line.textContent = text;
        term.appendChild(line);
        term.scrollTop = term.scrollHeight;
    };

    const clearTerminal = (terminalId) => {
        const term = document.getElementById(terminalId);
        term.innerHTML = '';
        term.classList.add('hidden');
    };

    // --- PHASE 1 ---
    
    // File Encryption
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');
    const encryptFileBtn = document.getElementById('encrypt-file-btn');
    const fileResults = document.getElementById('file-results');

    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileName.textContent = e.target.files[0].name;
            encryptFileBtn.disabled = false;
        } else {
            fileName.textContent = 'No file selected';
            encryptFileBtn.disabled = true;
        }
    });

    encryptFileBtn.addEventListener('click', async () => {
        const file = fileInput.files[0];
        if (!file) return;

        encryptFileBtn.textContent = 'Encrypting...';
        encryptFileBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE}/api/encrypt/file`, { method: 'POST', body: formData });
            if (!response.ok) throw new Error('Encryption failed');
            const data = await response.json();
            
            document.getElementById('aes-time').textContent = data.aes_time + 's';
            document.getElementById('des-time').textContent = data.des_time + 's';
            document.getElementById('aes-size').textContent = data.aes_size + ' bytes';
            document.getElementById('des-size').textContent = data.des_size + ' bytes';
            fileResults.classList.remove('hidden');
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            encryptFileBtn.textContent = 'Encrypt File';
            encryptFileBtn.disabled = false;
        }
    });

    // Avalanche Effect
    const avalancheBtn = document.getElementById('avalanche-btn');
    avalancheBtn.addEventListener('click', async () => {
        const plaintext = document.getElementById('avalanche-input').value;
        avalancheBtn.textContent = 'Calculating...';
        avalancheBtn.disabled = true;
        try {
            const response = await fetch(`${API_BASE}/api/phase1/avalanche`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ plaintext })
            });
            const data = await response.json();
            document.getElementById('ava-pt-diff').textContent = data.pt_diff_bits;
            document.getElementById('ava-pt-percent').textContent = data.pt_diff_percent + '%';
            document.getElementById('ava-key-diff').textContent = data.key_diff_bits;
            document.getElementById('ava-key-percent').textContent = data.key_diff_percent + '%';
            document.getElementById('avalanche-results').classList.remove('hidden');
        } catch (e) { alert(e); }
        finally {
            avalancheBtn.textContent = 'Calculate Avalanche Effect';
            avalancheBtn.disabled = false;
        }
    });

    // ECB vs CBC Image Leakage
    const imgInput = document.getElementById('image-input');
    const imgName = document.getElementById('image-name');
    const encryptImgBtn = document.getElementById('encrypt-image-btn');
    const imgResults = document.getElementById('image-results');

    imgInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            imgName.textContent = e.target.files[0].name;
            encryptImgBtn.disabled = false;
        } else {
            imgName.textContent = 'No image selected';
            encryptImgBtn.disabled = true;
        }
    });

    encryptImgBtn.addEventListener('click', async () => {
        const file = imgInput.files[0];
        if (!file) return;

        encryptImgBtn.textContent = 'Processing Image...';
        encryptImgBtn.disabled = true;

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE}/api/encrypt/image`, { method: 'POST', body: formData });
            if (!response.ok) throw new Error('Image processing failed');
            const data = await response.json();
            document.getElementById('img-orig').src = data.original;
            document.getElementById('img-ecb').src = data.ecb;
            document.getElementById('img-cbc').src = data.cbc;
            imgResults.classList.remove('hidden');
        } catch (error) { alert('Error: ' + error.message); }
        finally {
            encryptImgBtn.textContent = 'Process Image';
            encryptImgBtn.disabled = false;
        }
    });

    // Benchmark Payload Sizes
    const benchmarkBtn = document.getElementById('run-benchmark-btn');
    benchmarkBtn.addEventListener('click', async () => {
        benchmarkBtn.disabled = true;
        benchmarkBtn.textContent = 'Running...';
        clearTerminal('benchmark-terminal');
        try {
            const response = await fetch(`${API_BASE}/api/phase1/benchmark`);
            const data = await response.json();
            appendTerminal('benchmark-terminal', '=== BENCHMARK RESULTS (AES vs 3DES) ===\n', '#facc15');
            data.results.forEach(res => {
                appendTerminal('benchmark-terminal', `Size: ${res.size.toUpperCase()}`);
                appendTerminal('benchmark-terminal', `  AES  - Encrypt: ${res.aes_enc}s | Decrypt: ${res.aes_dec}s`, '#4ade80');
                appendTerminal('benchmark-terminal', `  3DES - Encrypt: ${res.des3_enc}s | Decrypt: ${res.des3_dec}s`, '#f87171');
                appendTerminal('benchmark-terminal', '--------------------------------------');
            });
        } catch (e) { appendTerminal('benchmark-terminal', 'Error: ' + e, 'red'); }
        finally {
            benchmarkBtn.disabled = false;
            benchmarkBtn.textContent = 'Run Benchmarks';
        }
    });

    // --- PHASE 2 ---
    const dhBtn = document.getElementById('dh-btn');
    dhBtn.addEventListener('click', async () => {
        dhBtn.disabled = true;
        clearTerminal('dh-terminal');
        appendTerminal('dh-terminal', 'Simulating Diffie-Hellman Key Exchange...', '#facc15');
        try {
            const res = await fetch(`${API_BASE}/api/phase2/dh-mitm`);
            const data = await res.json();
            appendTerminal('dh-terminal', '\n--- SECURE EXCHANGE ---', '#a855f7');
            appendTerminal('dh-terminal', `Alice Secret: ${data.secure.alice_secret}`);
            appendTerminal('dh-terminal', `Bob Secret:   ${data.secure.bob_secret}`);
            appendTerminal('dh-terminal', `Match? ${data.secure.match}`, data.secure.match ? '#4ade80' : 'red');

            appendTerminal('dh-terminal', '\n--- MAN-IN-THE-MIDDLE ATTACK ---', '#ef4444');
            appendTerminal('dh-terminal', `Alice derived secret: ${data.mitm.alice_thinks_secret_is}`);
            appendTerminal('dh-terminal', `Bob derived secret:   ${data.mitm.bob_thinks_secret_is}`);
            appendTerminal('dh-terminal', `Eve shared w/ Alice:  ${data.mitm.eve_secret_with_alice}`);
            appendTerminal('dh-terminal', `Eve shared w/ Bob:    ${data.mitm.eve_secret_with_bob}`);
            appendTerminal('dh-terminal', `Alice & Bob Match? ${data.mitm.alice_bob_match}`, 'red');
            appendTerminal('dh-terminal', 'Conclusion: Unauthenticated DH is vulnerable. Eve can read all traffic!', '#facc15');
        } catch (e) { appendTerminal('dh-terminal', e, 'red'); }
        finally { dhBtn.disabled = false; }
    });

    const rsaHybridBtn = document.getElementById('rsa-hybrid-btn');
    rsaHybridBtn.addEventListener('click', async () => {
        rsaHybridBtn.disabled = true;
        clearTerminal('rsa-hybrid-terminal');
        try {
            const res = await fetch(`${API_BASE}/api/phase2/rsa-hybrid`);
            const data = await res.json();
            appendTerminal('rsa-hybrid-terminal', 'Generated AES Session Key (Hex):');
            appendTerminal('rsa-hybrid-terminal', data.original_key, '#4ade80');
            appendTerminal('rsa-hybrid-terminal', '\nEncrypted with RSA Public Key (Truncated):');
            appendTerminal('rsa-hybrid-terminal', data.encrypted_key_preview, '#f87171');
            appendTerminal('rsa-hybrid-terminal', '\nDecrypted with RSA Private Key (Hex):');
            appendTerminal('rsa-hybrid-terminal', data.decrypted_key, '#4ade80');
            appendTerminal('rsa-hybrid-terminal', `\nKeys Match: ${data.match}`, '#facc15');
        } catch (e) { appendTerminal('rsa-hybrid-terminal', e, 'red'); }
        finally { rsaHybridBtn.disabled = false; }
    });

    // --- PHASE 3 ---
    const hashBtn = document.getElementById('hash-btn');
    hashBtn.addEventListener('click', async () => {
        const text = document.getElementById('hash-input').value || "Default input";
        clearTerminal('hash-terminal');
        try {
            const res = await fetch(`${API_BASE}/api/phase3/hash`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: text })
            });
            const data = await res.json();
            appendTerminal('hash-terminal', 'Input text:', '#facc15');
            appendTerminal('hash-terminal', text);
            appendTerminal('hash-terminal', '\nSHA-256 Digest:', '#facc15');
            appendTerminal('hash-terminal', data.hash, '#4ade80');
        } catch (e) { appendTerminal('hash-terminal', e, 'red'); }
    });

    const tamperBtn = document.getElementById('tamper-btn');
    tamperBtn.addEventListener('click', async () => {
        const text = document.getElementById('tamper-input').value;
        clearTerminal('tamper-terminal');
        try {
            const res = await fetch(`${API_BASE}/api/phase3/tamper-detect`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: text, tamper_index: 0 })
            });
            const data = await res.json();
            appendTerminal('tamper-terminal', `Original Data: ${data.original_data}`);
            appendTerminal('tamper-terminal', `Original Hash: ${data.original_hash}`, '#4ade80');
            appendTerminal('tamper-terminal', `\nTampered Data (1 byte flipped in transit):`);
            appendTerminal('tamper-terminal', data.tampered_data, '#ef4444');
            appendTerminal('tamper-terminal', `Tampered Hash: ${data.tampered_hash}`, '#ef4444');
            
            if (!data.match) {
                appendTerminal('tamper-terminal', '\n[!] ALERT: Tampering detected! Hash mismatch.', '#facc15');
            }
        } catch (e) { appendTerminal('tamper-terminal', e, 'red'); }
    });

    // --- PHASE 4 ---
    const sigBtn = document.getElementById('signature-btn');
    sigBtn.addEventListener('click', async () => {
        const text = document.getElementById('sig-input').value || "This transcript is verified and genuine.";
        clearTerminal('signature-terminal');
        try {
            const res = await fetch(`${API_BASE}/api/phase4/digital-signature`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ data: text })
            });
            const data = await res.json();
            appendTerminal('signature-terminal', `Generated RSA Signature (Truncated):`);
            appendTerminal('signature-terminal', data.signature_preview, '#a855f7');
            appendTerminal('signature-terminal', `\nVerifying Original Data...`);
            appendTerminal('signature-terminal', `Valid: ${data.valid_original}`, '#4ade80');
            
            appendTerminal('signature-terminal', `\nVerifying Tampered Data: "${data.tampered_data}"`);
            appendTerminal('signature-terminal', `Valid: ${data.valid_tampered}`, '#ef4444');
        } catch (e) { appendTerminal('signature-terminal', e, 'red'); }
    });

    const certBtn = document.getElementById('cert-btn');
    certBtn.addEventListener('click', async () => {
        clearTerminal('cert-terminal');
        try {
            const res = await fetch(`${API_BASE}/api/phase4/certificate`);
            const data = await res.json();
            appendTerminal('cert-terminal', '=== X.509 MOCK CERTIFICATE GENERATED ===', '#facc15');
            appendTerminal('cert-terminal', `Subject: ${data.subject}`);
            appendTerminal('cert-terminal', `Issuer: ${data.issuer}`);
            appendTerminal('cert-terminal', `Valid From: ${data.not_valid_before}`);
            appendTerminal('cert-terminal', `Valid To: ${data.not_valid_after}`);
            appendTerminal('cert-terminal', `Serial Number: ${data.serial_number}`);
            appendTerminal('cert-terminal', '\nCertificate PEM:');
            appendTerminal('cert-terminal', data.cert_pem, '#4ade80');
        } catch (e) { appendTerminal('cert-terminal', e, 'red'); }
    });

    const kerbBtn = document.getElementById('kerberos-btn');
    kerbBtn.addEventListener('click', async () => {
        kerbBtn.disabled = true;
        clearTerminal('kerberos-terminal');
        try {
            const res = await fetch(`${API_BASE}/api/phase4/kerberos`);
            const data = await res.json();
            appendTerminal('kerberos-terminal', '=== KERBEROS AUTHENTICATION GATE ===\n', '#facc15');
            for (let i = 0; i < data.steps.length; i++) {
                appendTerminal('kerberos-terminal', data.steps[i], i === data.steps.length - 1 ? '#4ade80' : '#38bdf8');
                await new Promise(r => setTimeout(r, 600)); // Simulate delay for effect
            }
        } catch (e) { appendTerminal('kerberos-terminal', e, 'red'); }
        finally { kerbBtn.disabled = false; }
    });

    // --- PHASE 5 ---
    const startSimBtn = document.getElementById('start-simulation');
    const serverTerminal = document.getElementById('server-terminal');
    const clientTerminal = document.getElementById('client-terminal');

    startSimBtn.addEventListener('click', () => {
        serverTerminal.innerHTML = '';
        clientTerminal.innerHTML = '';
        startSimBtn.disabled = true;
        startSimBtn.textContent = 'Simulating...';

        const ws = new WebSocket('ws://127.0.0.1:8000/ws/simulate');

        // Fallback if hosted on different port locally:
        // const ws = new WebSocket('ws://127.0.0.1:8000/ws/simulate');

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const line = document.createElement('div');
            line.className = 'log-line';
            
            if (data.message.includes('FAILED') || data.message.includes('Error')) {
                line.style.color = '#ef4444';
            } else if (data.message.includes('PASSED') || data.message.includes('SUCCESS') || data.message.includes('OK')) {
                line.style.color = '#4ade80';
            } else if (data.message.includes('Phase')) {
                line.style.color = '#facc15';
            } else {
                line.style.color = '#38bdf8';
            }

            line.textContent = data.message;

            if (data.role === 'server') {
                serverTerminal.appendChild(line);
                serverTerminal.scrollTop = serverTerminal.scrollHeight;
            } else if (data.role === 'client') {
                clientTerminal.appendChild(line);
                clientTerminal.scrollTop = clientTerminal.scrollHeight;
            }
        };

        ws.onclose = () => {
            startSimBtn.disabled = false;
            startSimBtn.textContent = 'Initiate Secure Exchange';
        };
        
        ws.onerror = (error) => {
            console.error('WebSocket Error:', error);
            const line = document.createElement('div');
            line.className = 'log-line';
            line.style.color = '#ef4444';
            line.textContent = 'Connection error. Is the backend running?';
            serverTerminal.appendChild(line);
            startSimBtn.disabled = false;
            startSimBtn.textContent = 'Initiate Secure Exchange';
        };
    });
});
