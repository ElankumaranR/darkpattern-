chrome.action.onClicked.addListener((tab) => {
  chrome.windows.create({
      type: 'popup',
      url: 'popup.html',
      width: 400,
      height: 400,
      left: (screen.width / 2) - (400 / 2),
      top: (screen.height / 2) - (400 / 2)
  });
});

chrome.runtime.onMessage.addListener(function(message, sender, sendResponse){
  if(message.action === 'analise'){
      chrome.tabs.query({ active: true, currentWindow: true }, function(tabs){
          var activetab = tabs[0];
          chrome.scripting.executeScript({
              target: { tabId: activetab.id },
              function: scrapeContent
          });
      });
  }
});

function scrapeContent() {
  var htmlcontent = document.documentElement.outerHTML;
  if(htmlcontent != null)
      fetch('http://localhost:5000/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ htmlcontent: htmlcontent })
      })
      .then(response => response.json())
      .then(data => {
          console.log('Response from server:', data);
          var sentences = data.result;
          var keys = Object.keys(sentences);
          var len = keys.length;
          chrome.runtime.sendMessage({ action: 'no_of_darkpattern', data: len });
          keys.forEach(key => {
            const sentence = key;
            const regex = new RegExp(sentence, 'gi');
            const hoverText = sentences[key]; 
            document.body.innerHTML = document.body.innerHTML.replace(regex, `<span style='background-color: yellow' title='${hoverText}'>$&</span>`);
        });
        })
      .catch(error => {
          console.error('Error sending HTML content to server:', error);
      });
  else
      console.log("Error in getting html content");
}


