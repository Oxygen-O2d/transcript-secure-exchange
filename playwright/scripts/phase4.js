const { setupBrowser } = require('./helper');

async function run() {
    console.log("Launching Phase 4 Demo...");
    const { browser, page } = await setupBrowser();
    
    await page.click("text=04");
    
    console.log("Generating Digital Signature...");
    await page.click("text=▶ SIGN DOCUMENT");
    await page.waitForTimeout(2000);
    
    console.log("Generating X.509 Certificate...");
    await page.click("text=▶ GENERATE CERTIFICATE");
    await page.waitForTimeout(2000);
    
    console.log("Simulating Kerberos...");
    await page.click("text=▶ SIMULATE KERBEROS");
    await page.waitForTimeout(6000);

    await browser.close();
}

run().catch(console.error);
