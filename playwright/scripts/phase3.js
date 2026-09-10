const { setupBrowser } = require('./helper');

async function run() {
    console.log("Launching Phase 3 Demo...");
    const { browser, page } = await setupBrowser();
    
    await page.click("text=03");
    
    console.log("Computing SHA-256 Hash...");
    await page.fill("textarea#p3-data", "Final Grade: A");
    await page.click("text=▶ COMPUTE HASH");
    await page.waitForTimeout(2000);
    
    console.log("Simulating Tampering...");
    await page.fill("input#p3-tamp", "Final Grade: F");
    await page.click("text=SIMULATE TAMPERING");
    await page.waitForTimeout(4000);

    await browser.close();
}

run().catch(console.error);
