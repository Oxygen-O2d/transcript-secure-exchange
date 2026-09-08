document.addEventListener('DOMContentLoaded', () => {
    // Navigation
    const navLinks = document.querySelectorAll('.nav-links li');
    const sections = document.querySelectorAll('.view-section');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Update active state
            navLinks.forEach(l => l.classList.remove('active'));
            link.classList.add('active');

            // Show target section
            const targetId = link.getAttribute('data-target');
            sections.forEach(sec => sec.classList.remove('active'));
            document.getElementById(targetId).classList.add('active');
        });
    });

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
            const response = await fetch('http://127.0.0.1:8000/api/encrypt/file', {
                method: 'POST',
                body: formData
            });

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

    // Image Encryption (ECB vs CBC)
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
            const response = await fetch('http://127.0.0.1:8000/api/encrypt/image', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Image processing failed');

            const data = await response.json();
            
            document.getElementById('img-orig').src = data.original;
            document.getElementById('img-ecb').src = data.ecb;
            document.getElementById('img-cbc').src = data.cbc;
            
            imgResults.classList.remove('hidden');
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            encryptImgBtn.textContent = 'Encrypt Image';
            encryptImgBtn.disabled = false;
        }
    });

    // Simulation Phase
    const startSimBtn = document.getElementById('start-simulation');
    const serverTerminal = document.getElementById('server-terminal');
    const clientTerminal = document.getElementById('client-terminal');

    startSimBtn.addEventListener('click', () => {
        // Clear terminals
        serverTerminal.innerHTML = '';
        clientTerminal.innerHTML = '';
        
        startSimBtn.disabled = true;
        startSimBtn.textContent = 'Simulating...';

        const ws = new WebSocket('ws://127.0.0.1:8000/ws/simulate');

        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const line = document.createElement('div');
            line.className = 'log-line';
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
            line.style.color = 'red';
            line.textContent = 'Connection error. Is the backend running?';
            serverTerminal.appendChild(line);
            startSimBtn.disabled = false;
            startSimBtn.textContent = 'Initiate Secure Exchange';
        };
    });
});
