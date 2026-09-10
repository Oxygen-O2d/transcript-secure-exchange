const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const DUMMY_TXT_PATH = path.join(__dirname, '..', 'dummy.txt');
const DUMMY_IMG_PATH = path.join(__dirname, '..', 'dummy.png');
const FRONTEND_PATH = path.join(__dirname, '..', '..', 'frontend', 'index.html');
const FILE_URI = `file:///${FRONTEND_PATH.replace(/\\/g, '/')}`;

// Ensure dummy files exist
function ensureDummyFiles() {
    if (!fs.existsSync(DUMMY_TXT_PATH)) {
        fs.writeFileSync(DUMMY_TXT_PATH, "This is a dummy transcript file for benchmarking AES and 3-DES encryption speeds.");
    }
    if (!fs.existsSync(DUMMY_IMG_PATH)) {
        const b64_png = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
        fs.writeFileSync(DUMMY_IMG_PATH, Buffer.from(b64_png, 'base64'));
    }
}

async function setupBrowser() {
    ensureDummyFiles();
    // Using 'msedge' channel to use the system's Microsoft Edge browser
    // This prevents Windows Application Control policies from blocking the local Chromium binary.
    const browser = await chromium.launch({ 
        headless: false, 
        slowMo: 700,
        channel: 'msedge' 
    });
    const page = await browser.newPage();
    await page.goto(FILE_URI);
    return { browser, page };
}

module.exports = {
    setupBrowser,
    DUMMY_TXT_PATH,
    DUMMY_IMG_PATH
};
