const { setupBrowser } = require('./helper');

async function run() {
    console.log("Launching Phase 5 Demo...");
    const { browser, page } = await setupBrowser();
    
    await page.click("text=05");
    
    console.log("Starting Full Transmission Simulation...");
    await page.click("text=▶ RUN COMPLETE PIPELINE");
    
    // Wait for the WebSocket simulation to finish
    console.log("Watching the End-to-End Pipeline...");
    await page.waitForTimeout(14000);
    
    await browser.close();
}

run().catch(console.error);
