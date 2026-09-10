const { setupBrowser } = require('./helper');

async function run() {
    console.log("Launching Phase 2 Demo...");
    const { browser, page } = await setupBrowser();
    
    await page.click("text=02");
    
    console.log("Simulating RSA Hybrid Exchange...");
    await page.click("text=▶ GENERATE & ENCRYPT KEY");
    await page.waitForTimeout(4000);
    
    console.log("Simulating Diffie-Hellman & MITM...");
    await page.click("text=▶ EXECUTE EXCHANGE");
    await page.waitForTimeout(2000);
    
    await page.click("text=SIMULATE MITM");
    await page.waitForTimeout(4000);

    await browser.close();
}

run().catch(console.error);
