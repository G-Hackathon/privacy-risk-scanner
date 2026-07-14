const scanCache = new Map();

const CACHE_TIME = 5 * 60 * 1000; // 5 minutes

chrome.tabs.onActivated.addListener(async (activeInfo) => {

    try {

        const tab = await chrome.tabs.get(activeInfo.tabId);

        if (!tab.url) return;

        scanWebsite(tab.url);

    } catch (e) {

        console.log(e);

    }

});

chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {

    if (changeInfo.status !== "complete") return;

    if (!tab.url) return;

    scanWebsite(tab.url);

});

async function scanWebsite(url) {

    if (
        url.startsWith("chrome://") ||
        url.startsWith("edge://") ||
        url.startsWith("about:")
    ) {
        return;
    }

    const cached = scanCache.get(url);

    if (cached) {

        const age = Date.now() - cached.time;

        if (age < CACHE_TIME) {

            console.log("Using cached scan:", url);

            return;

        }

    }

    try {

        const response = await fetch(
            "http://127.0.0.1:5000/scan",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url
                })

            }
        );

        const result = await response.json();

        scanCache.set(url, {

            time: Date.now(),

            result: result

        });

        console.log("Privacy Scan Complete");

        console.log(result);

    }

    catch (err) {

        console.log("Backend unavailable.");

    }

}