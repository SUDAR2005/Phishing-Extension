document.getElementById('checkButton').addEventListener('click', function() {
    console.log("Hello")
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        const activeTab = tabs[0];
        const activeTabURL = activeTab.url;

        chrome.runtime.sendMessage({url: activeTabURL}, function(response) {
            const resultDiv = document.getElementById('result');
            if (response.isFake) {
                resultDiv.textContent = 'This website is identified as fake!';
                resultDiv.style.color = 'red';
            } else {
                resultDiv.textContent = 'This website is safe!';
                resultDiv.style.color = 'green';
            }
        });
    });
});
