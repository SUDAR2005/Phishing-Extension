chrome.runtime.onMessage.addListener((message, sender, sendResponse) =>{
  if (message.action === 'checkUrl'){
    const url = message.url;
    console.log(url);
    fetch('http://localhost:5000/predict',{
      method: 'POST',
      headers:{
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data =>{
      console.log("Background.js " + data);
      chrome.tabs.sendMessage(message.id,{ action: 'checkPage', isFake: data.isFake });
      
      // Send the response back to popup.js
      sendResponse({ isFake: data.isFake });
    })
    .catch(error =>{
      console.error('Error:', error);

      // Send an error response back to popup.js
      sendResponse({ error: 'Failed to process the URL' });
    });

    // Return true to indicate that we will respond asynchronously
    return true;
  }
});
