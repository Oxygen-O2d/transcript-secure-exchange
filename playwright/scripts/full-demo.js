const { setupBrowser, DUMMY_TXT_PATH, DUMMY_IMG_PATH } = require('./helper');

async function run() {
    console.log("Launching Playwright Full Demo...");
    const { browser, page } = await setupBrowser();
    
    // ======== PHASE 1 ========
    console.log("Navigating to Phase 1...");
    await page.click("text=01");
    
    console.log("Running AES vs 3-DES Benchmark...");
    await page.setInputFiles("input#p1-file", DUMMY_TXT_PATH);
    await page.click("text=▶ RUN BENCHMARK");
    await page.waitForTimeout(2000); // Pause for audience
    
    console.log("Running ECB vs CBC Image Pattern test...");
    await page.locator('.card:has-text("ECB vs CBC")').scrollIntoViewIfNeeded();
    await page.setInputFiles("input#p1-image", DUMMY_IMG_PATH);
    await page.waitForSelector('#img-ecb', { state: 'visible' }); // Wait for photo to show
    await page.waitForTimeout(2000); // Wait 2 seconds for teacher to see
    
    console.log("Running Avalanche Effect Analysis...");
    await page.fill("input#av-modified", "Changing one bit changes everything");
    await page.click("text=▶ ANALYZE BITS");
    await page.waitForTimeout(2000);

    // ======== PHASE 2 ========
    console.log("Navigating to Phase 2...");
    await page.click("text=02");
    
    console.log("Simulating RSA Hybrid Exchange...");
    await page.click("text=▶ GENERATE & ENCRYPT KEY");
    await page.waitForTimeout(4000);
    
    console.log("Simulating Diffie-Hellman & MITM...");
    await page.click("text=▶ EXECUTE EXCHANGE");
    await page.waitForTimeout(2000);
    await page.click("text=SIMULATE MITM");
    await page.waitForTimeout(2000);

    // ======== PHASE 3 ========
    console.log("Navigating to Phase 3...");
    await page.click("text=03");
    
    console.log("Computing SHA-256 Hash...");
    await page.fill("textarea#p3-data", "Final Grade: A");
    await page.click("text=▶ COMPUTE HASH");
    await page.waitForTimeout(2000);
    
    console.log("Simulating Tampering...");
    await page.fill("input#p3-tamp", "Final Grade: F");
    await page.click("text=SIMULATE TAMPERING");
    await page.waitForTimeout(2000);

    // ======== PHASE 4 ========
    console.log("Navigating to Phase 4...");
    await page.click("text=04");
    
    console.log("Generating Digital Signature...");
    await page.click("text=▶ SIGN DOCUMENT");
    await page.waitForTimeout(2000);
    
    console.log("Generating X.509 Certificate...");
    await page.click("text=▶ GENERATE CERTIFICATE");
    await page.waitForTimeout(2000);
    
    console.log("Simulating Kerberos...");
    await page.click("text=▶ SIMULATE KERBEROS");
    await page.waitForTimeout(5000);

    // ======== PHASE 5 ========
    console.log("Navigating to Phase 5...");
    await page.click("text=05");
    
    console.log("Starting Full Transmission Simulation...");
    await page.click("text=▶ RUN COMPLETE PIPELINE");
    
    // Wait for the WebSocket simulation to finish
    console.log("Watching the End-to-End Pipeline...");
    await page.waitForTimeout(12000);
    
    console.log("Demo completed successfully! Closing in 3 seconds...");
    await page.waitForTimeout(3000);
    await browser.close();
}

run().catch(console.error);
