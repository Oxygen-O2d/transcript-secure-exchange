const { setupBrowser, DUMMY_TXT_PATH, DUMMY_IMG_PATH } = require('./helper');

async function run() {
    console.log("Launching Phase 1 Demo...");
    const { browser, page } = await setupBrowser();
    
    await page.click("text=01");
    
    console.log("Running AES vs 3-DES Benchmark...");
    await page.setInputFiles("input#p1-file", DUMMY_TXT_PATH);
    await page.click("text=▶ RUN BENCHMARK");
    await page.waitForTimeout(2000);
    
    console.log("Running ECB vs CBC Image Pattern test...");
    await page.locator('.card:has-text("ECB vs CBC")').scrollIntoViewIfNeeded();
    await page.setInputFiles("input#p1-image", DUMMY_IMG_PATH);
    await page.waitForSelector('#img-ecb', { state: 'visible' }); // Wait for photo to show
    await page.waitForTimeout(2000); // Wait 2 seconds for teacher to see
    
    console.log("Running Avalanche Effect Analysis...");
    await page.fill("input#av-modified", "Changing one bit changes everything");
    await page.click("text=▶ ANALYZE BITS");
    await page.waitForTimeout(4000);

    await browser.close();
}

run().catch(console.error);
