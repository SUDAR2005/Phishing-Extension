document.addEventListener('DOMContentLoaded',function(){
    const checkButton = document.getElementById('checkButton');
    if (checkButton){
        checkButton.addEventListener('click',function(){
            console.log("Button clicked");
            chrome.tabs.query({ active: true,currentWindow: true },function(tabs){
                const activeTab = tabs[0];
                const activeTabURL = document.getElementById("input-box").innerText;
                console.log(activeTab)
                console.log(activeTab.id)
                chrome.runtime.sendMessage({ action: 'checkUrl',url: activeTabURL,id: activeTab.id },function(response){
                    console.log("Response received:",response);
                    const resultDiv = document.getElementById('result');
                    if (response && response.isFake !== undefined){
                        if (response.isFake){
                            resultDiv.textContent = 'This website is identified as a Phishing Site!';
                            resultDiv.style.color = 'red';
                        } else{
                            resultDiv.textContent = 'This website is safe!';
                            resultDiv.style.color = 'green';
                        }
                    } else{
                        console.error('Unexpected response format:',response);
                        resultDiv.textContent = 'Error processing response.';
                        resultDiv.style.color = 'orange';
                    }
                });
            });
        });
    } else{
        console.error('Button element not found.');
    }
});
