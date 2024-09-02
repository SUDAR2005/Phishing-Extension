chrome.runtime.onMessage.addListener((message, sender, sendResponse)=>{
  if (message.action === 'checkUrl') {
    const url = message.url;
    console.log(url)
    fetch('http://localhost:5000/predict', {
      method:'POST',
      headers:{
        'Content-Type':'application/json'
      },
      body:JSON.stringify({ url:url })
    })
    .then(response=>response.json())
    .then(data=>{
      console.log(data)
      chrome.tabs.sendMessage(sender.tab.id, {action:'checkPage', isFake:data.isFake});
    })
    .catch(error=>console.error('Error:', error));
  }
});
