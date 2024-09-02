// Listen for messages from the background script
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
    if (request.action === 'checkPage') {
        const isFake = request.isFake;
        console.log(isFake)

        if (isFake) {
            // Create and style a warning banner
            const warningBanner = document.createElement('div');
            warningBanner.style.backgroundColor = 'red';
            warningBanner.style.color = 'white';
            warningBanner.style.position = 'fixed';
            warningBanner.style.top = '0';
            warningBanner.style.left = '0';
            warningBanner.style.width = '100%';
            warningBanner.style.zIndex = '1000';
            warningBanner.style.padding = '10px';
            warningBanner.style.textAlign = 'center';
            warningBanner.textContent = 'Warning: This website is suspected to be fake!';
            
            // Append the banner to the top of the page
            document.body.prepend(warningBanner);
        }
    }
});

// Send the current URL to the background script
chrome.runtime.sendMessage({action: 'checkUrl', url: window.location.href});

