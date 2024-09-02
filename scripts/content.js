chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
    if (request.action === 'checkPage'){
        const isFake=request.isFake;
        console.log(isFake)

        if (isFake){
            const warningBanner=document.createElement('div');
            warningBanner.style.backgroundColor='red';
            warningBanner.style.color='white';
            warningBanner.style.position='fixed';
            warningBanner.style.top='0';
            warningBanner.style.left='0';
            warningBanner.style.width='100%';
            warningBanner.style.zIndex='1000';
            warningBanner.style.padding='10px';
            warningBanner.style.textAlign='center';
            warningBanner.textContent='Warning: This website is suspected to be fake!';
            document.body.prepend(warningBanner);
        }
    }
});
chrome.runtime.sendMessage({action: 'checkUrl', url: window.location.href});

