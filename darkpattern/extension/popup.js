document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("analyzeButton").addEventListener("click", function() {
        chrome.runtime.sendMessage({action:'analise'});    });
});
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.action === 'no_of_darkpattern') {
        document.getElementById('no_of_darkpattern').innerHTML=message.data;
    }
});