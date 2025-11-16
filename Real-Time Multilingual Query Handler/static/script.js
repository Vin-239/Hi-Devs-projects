document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('translateButton').addEventListener('click', () => {
        
        const text = document.getElementById('inputText').value;
        const resultDiv = document.getElementById('result-container');

        console.log("Sending text to server:", text);

        resultDiv.textContent = 'Translating...';

        fetch('/translate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: text,
            })
        })
        .then(response => response.json())
        .then(data => {
            
            console.log("Received data from server:", data);

            if (data.translation) {
                resultDiv.textContent = data.translation;
            } else if (data.error) {
                resultDiv.textContent = 'Error: ' + data.error;
            }
        })
        .catch(error => {
            console.error("Fetch failed:", error); 
            resultDiv.textContent = 'Request failed: ' + error;
        });
    });

});