function showScenario() {
    document.getElementById('scenario').style.display = 'block';
    document.getElementById('summary').style.display = 'none';
}

function showSummary() {
    document.getElementById('scenario').style.display = 'none';
    document.getElementById('summary').style.display = 'block';
}

// Implement the Python link for sendButton
document.getElementById('sendButton').addEventListener('click', function() {
    const userInput = document.getElementById('userInput').value;
    // Here, you would call your Python backend with the userInput
    // Example (requires backend setup):
    // fetch('/send_message', {
    //     method: 'POST',
    //     body: JSON.stringify({ message: userInput }),
    //     headers: {
    //         'Content-Type': 'application/json'
    //     }
    // }).then(response => response.json()).then(data => {
    //     console.log(data);
    // });
});

document.getElementById('nextButton').addEventListener('click', function() {
    showSummary();
    // Here you might also want to handle passing data to the summary page.
});

// Implement Voice Input Start/Stop
document.getElementById('startVoiceButton').addEventListener('click', function() {
    // Code to start voice input
});

document.getElementById('stopVoiceButton').addEventListener('click', function() {
    // Code to stop voice input
});
