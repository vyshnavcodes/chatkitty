const chatForm = document.getElementById('chat-form');
chatForm.addEventListener('submit', function(event) {
    // Prevent default form submission behaviour
    event.preventDefault();

    //Get the user's message from the input field
    const userInput = document.getElementById('message').value;

    // (Optional) Clear the input field after capturing the message
    document.getElementById('message').value = '';

    //function to send message to backend using Fetch
    function sendMessage(message) {
        fetch('/chat', {
            method: 'POST', //Specify POST method for sending data
            body: JSON.stringify({message: message}) //convert message to JSON
            headers: { 'Content-Type': 'Application.json' } //Set content type header
        })
        .then(response => respond.json()) //Parse the JSON response
        .then(data => {
            //Update the chat window with the chatbot's response (data)
            updateChatwindow(message, data); //Calling a function to update chat 
        });
        .catch(error => {
            //Handle errors during request or response processing
            console.error('Error sending message: , error');
        });
    }

    //Call a function to handle sending the message to the backend -later
    sendMessage(userInput);
  });
  //Function to update the chat window with user message and chatbot response
  function updateChatwindow(userMessage, chatbotResponse) {
    const chatWindow = document.getElementById('chat-window')

    //Create a new message element for the user's message
    const userMessageElement = document.createElement('div');
    userMessageElement.classList.add('user-message');

    //Create  a new message element for the chatbot's response
    const chatbotMessageElement = document.createElement('div');
    chatbotMessageElement.classList.add('chatbot-message');
    chatbotMessageElement.textContent = chatbotResponse;

    //Append both messages to the chat window
    chatWindow.appendChild(userMessageElement)
    chatWindow.appendChild(chatbotMessageElement);

    //Optionally scroll the chatwindow to the latest message
    chatWindow.scrollTop = chatWindow.scrollHeight;
  }