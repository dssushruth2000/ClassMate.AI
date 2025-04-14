let greeted = false; // Global flag

// function toggleChat() {
//     var chatWindow = document.getElementById("chat-window");
//     const isHidden = chatWindow.style.display === "none" || chatWindow.style.display === "";

//     chatWindow.style.display = isHidden ? "flex" : "none";

//     // Send greeting only the first time it opens
//     if (isHidden && !greeted) {
//         greeted = true;
//         const chatBody = document.getElementById("chat-body");
//         const typing = document.createElement("div");
//         typing.classList.add("bot-message");
//         typing.innerText = "⏳ Bot is typing...";
//         chatBody.appendChild(typing);
//         chatBody.scrollTop = chatBody.scrollHeight;
        

//         setTimeout(() => {
//             chatBody.removeChild(typing);
//             displayMessage("Beep boop 🤖... just kidding.", "bot-message");
    
//             setTimeout(() => {
//                 displayMessage("I’m the UWM Chatbot — what can I dig up for you today?", "bot-message");
//             }, 1000); // Delay between two lines
//         }, 1000); // Delay before first greeting
//     }

//     // chatWindow.style.display = (chatWindow.style.display === "none" || chatWindow.style.display === "") ? "flex" : "none";
// }

function toggleChat() {
    const chatWindow = document.getElementById("chat-window");
    const isHidden = chatWindow.style.display === "none" || chatWindow.style.display === "";

    if (isHidden) {
        // Show and animate in
        chatWindow.style.display = "flex";
        chatWindow.classList.remove("closing");
        chatWindow.classList.add("opening");

        // Send greeting only the first time
        if (!greeted) {
            greeted = true;
            const chatBody = document.getElementById("chat-body");

            const typing = document.createElement("div");
            typing.classList.add("bot-message");
            typing.innerText = "⏳ Bot is typing...";
            chatBody.appendChild(typing);
            chatBody.scrollTop = chatBody.scrollHeight;

            setTimeout(() => {
                chatBody.removeChild(typing);
                displayMessage("Beep boop 🤖... just kidding.", "bot-message");

                setTimeout(() => {
                    // displayMessage("I’m the UWM Chatbot — what can I dig up for you today?", "bot-message");
                    displayMessage("I’m the UWM Chatbot — here to help you with anything related to the **Computer Science Department**! 💻📚", "bot-message");
                }, 1000);
            }, 1000);
        }

    } else {
        // Animate out
        chatWindow.classList.remove("opening");
        chatWindow.classList.add("closing");

        setTimeout(() => {
            chatWindow.style.display = "none";
        }, 300); // Match the animation duration in CSS
    }
}

// Send message on Enter key press
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function sendMessage() {
    var userInput = document.getElementById("user-input");
    var message = userInput.value.trim();

    if (message === "") return;


    // Display user message
    displayMessage(message, "user-message");

    // Clear input field
    userInput.value = "";

    const keywords = ["appointment", "book a meeting", "schedule"];
    const lowerMsg = message.toLowerCase();

    if (keywords.some(word => lowerMsg.includes(word))) {
    displayMessage(`Sure! Click below to schedule an appointment:<br>
        <button onclick="showAppointmentForm()" class="chat-appointment-btn">📅 Book Now</button>`, "bot-message");
    return;
    }



    // // 🟡 If user mentions "appointment", show form & skip API
    // if (message.toLowerCase().includes("appointment")) {
    //     displayMessage(`Sure! Click below to schedule an appointment:<br>
    //         <button onclick="showAppointmentForm()" class="chat-appointment-btn">📅 Book Now</button>`, "bot-message");
    //     return; // Stop here — don’t send to Flask
    // }

    // Show typing indicator
    // var chatBody = document.getElementById("chat-body");
    // var typingIndicator = document.createElement("div");
    // typingIndicator.classList.add("bot-message");
    // typingIndicator.innerText = "Bot is typing...";
    // chatBody.appendChild(typingIndicator);
    // chatBody.scrollTop = chatBody.scrollHeight;

    // Show animated typing indicator
    // var chatBody = document.getElementById("chat-body");
    // var typingIndicator = document.createElement("div");
    // typingIndicator.classList.add("bot-message", "typing");

    // var typingBubble = document.createElement("div");
    // typingBubble.classList.add("message-bubble");

    // typingBubble.innerText = "⏳ Bot is typing...";
    // typingIndicator.appendChild(typingBubble);
    // chatBody.appendChild(typingIndicator);

    var chatBody = document.getElementById("chat-body");
    const typingIndicator = document.createElement("div");
    typingIndicator.className = "chat-message bot-message typing-indicator";

    const typingBubble = document.createElement("div");
    typingBubble.className = "message-bubble typing";

    for (let i = 0; i < 3; i++) {
    const dot = document.createElement("span");
    dot.className = "dot";
    typingBubble.appendChild(dot);
    }

    typingIndicator.appendChild(typingBubble);
    chatBody.appendChild(typingIndicator);


    // Scroll to bottom
    setTimeout(() => {
    chatBody.scrollTo({
        top: chatBody.scrollHeight,
        behavior: "smooth"
    });
    }, 0);

    // Send request to Flask API
    fetch("/chatbot", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: message })
    })
    .then(response => response.json())
    .then(data => {
        chatBody.removeChild(typingIndicator);  // Remove typing indicator
        displayMessage(data.response, "bot-message");
        playSound("receive");
    })
    .catch(error => {
        chatBody.removeChild(typingIndicator);
        displayMessage("Error: Could not reach chatbot", "bot-message");
        console.error("Error:", error);
    });
}

function showAppointmentForm() {
    const chatBody = document.getElementById("chat-body");
    const hiddenForm = document.getElementById("hidden-appointment-form");

    // Clone the form so we can insert it into the flow
    const clonedForm = hiddenForm.firstElementChild.cloneNode(true);

    chatBody.appendChild(clonedForm);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function submitAppointment(event) {
    event.preventDefault(); // Stop normal form submission

    const form = event.target;

    const formData = new FormData(form);

    fetch('/submit_appointment', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(msg => {
        // Optional: remove the form after submission
        form.closest(".chat-message").remove();

        // Show confirmation in chatbot
        displayMessage("✅ Your appointment has been submitted successfully!", "bot-message");
    })
    .catch(error => {
        displayMessage("❌ Oops! Something went wrong while booking.", "bot-message");
        console.error("Error submitting appointment:", error);
    });
}

//Use this below if you want typing response like chatgpt oresle remove this function
function typeBotResponse(element, text, onComplete, speed = 10) {
    let i = 0;
    function typeChar() {
        if (i < text.length) {
            element.innerText += text.charAt(i);  // plain text typing
            i++;

            // Scroll the chat container while typing
            document.getElementById("chat-body").scrollTo({
                top: document.getElementById("chat-body").scrollHeight,
                behavior: "smooth"
            });

            setTimeout(typeChar, speed);
        } else if (onComplete) {
            onComplete();  // Replace raw text with full rich HTML
        }
    }
    typeChar();
}





function displayMessage(text, className) {
    const chatBody = document.getElementById("chat-body");

    // Create main message container
    const messageDiv = document.createElement("div");
    messageDiv.classList.add("chat-message", className);

    // Avatar
    const avatar = document.createElement("img");
    avatar.classList.add("avatar");
    avatar.src = className === "user-message"
        ? "static/avatar/User_Avatar.svg"
        : "static/avatar/Chatbot_Avatar.jpg";

    // Message content container
    // const messageContent = document.createElement("div");

    // Convert Markdown using Showdown
    const converter = new showdown.Converter({ openLinksInNewWindow: true });

    // ⛏️ Remove triple backtick code block wrapper (if any)
    text = text.replace(/```(?:\w*\n)?([\s\S]*?)```/, '$1');

    let html = converter.makeHtml(text);
    html = html.replace(/(^|[^">])(https?:\/\/[^\s)]+)/g, '$1<a href="$2" target="_blank">$2</a>');
    html = html.replace(/\n/g, "<br>");
    // messageContent.innerHTML = html.trim();

    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");
    // bubble.innerHTML = html.trim(); //orelse uncomment this if you remove the below one

    //Use this below if you want typing response like chatgpt
    bubble.textContent = ""; // Start empty
    if (className === "bot-message") {
        typeBotResponse(bubble, text, () => {
            // After typing ends, convert Markdown to HTML and render properly
            let html = converter.makeHtml(text);
            html = html.replace(/(^|[^">])(https?:\/\/[^\s)]+)/g, '$1<a href="$2" target="_blank">$2</a>');
            html = html.replace(/\n/g, "<br>");
            bubble.innerHTML = html.trim();

             // 🟡 Scroll again after rich HTML is rendered
             requestAnimationFrame(() => {
                setTimeout(() => {
                  document.getElementById("chat-body").scrollTo({
                    top: document.getElementById("chat-body").scrollHeight,
                    behavior: "smooth"
                  });
                }, 20); // You can experiment with delay between 10–30ms
            });
        });        
    } else {
        bubble.innerHTML = html.trim();
    }
    // uptill here - typing response code

    // Force a reflow (browser recalculates layout & events)-- still not confirmed workinh or not, if not remove this
    bubble.offsetHeight;
    

    // Append content in order based on message type
    if (className === "user-message") {
        messageDiv.appendChild(avatar); // Avatar on right
        messageDiv.appendChild(bubble);
        // messageDiv.appendChild(messageContent);
        // messageDiv.appendChild(avatar); // Avatar on right
    } else {
        messageDiv.appendChild(avatar); // Avatar on left
        // messageDiv.appendChild(messageContent);
        messageDiv.appendChild(bubble);
    }

    chatBody.appendChild(messageDiv);
    // chatBody.scrollTop = chatBody.scrollHeight;
    // Use setTimeout to defer scroll until after DOM update-- still not confirmed workinh or not
    setTimeout(() => {
        chatBody.scrollTo({
          top: chatBody.scrollHeight,
          behavior: "smooth"
        });
      }, 0);
      
}

document.addEventListener("DOMContentLoaded", () => {
    const chatBody = document.getElementById("chat-body");
    const scrollBtn = document.getElementById("scroll-to-bottom");
  
    // Show scroll button only if user scrolls up
    chatBody.addEventListener("scroll", () => {
        setTimeout(() => {
          const isUserScrolledUp = chatBody.scrollTop + chatBody.clientHeight < chatBody.scrollHeight - 20;
          scrollBtn.style.display = isUserScrolledUp ? "block" : "none";
        }, 450);  // Small delay (tweak as needed)
    });
      
  
    // Scroll to bottom when button is clicked
    scrollBtn.addEventListener("click", () => {
      chatBody.scrollTo({
        top: chatBody.scrollHeight,
        behavior: "smooth"
      });
  
      // Optional: auto-hide after scroll
      setTimeout(() => {
        scrollBtn.style.display = "none";
      }, 800);
    });
  });
  
  

function playSound(type) {
    const sounds = {
        // send: 'static/sounds/send.mp3',
        receive: 'static/sounds/receive.mp3',
        // success: 'static/sounds/success.mp3',
        // error: 'static/sounds/error.mp3'
    };

    const audio = new Audio(sounds[type]);
    audio.play();
}




// this functuion uses Showdown method and easy--in this clciking link is soved and use this if not adding avatar
// function displayMessage(text, className) {
//     var chatBody = document.getElementById("chat-body");
//     var messageDiv = document.createElement("div");
//     messageDiv.classList.add("chat-message", className);

//     // Configure Showdown to add target="_blank" automatically
//     var converter = new showdown.Converter({
//         openLinksInNewWindow: true // ✅ Ensures all links open in a new tab
//     });

//     text = converter.makeHtml(text); // Convert Markdown to HTML

//     // ✅ Convert raw URLs into clickable links (only if not inside Markdown)
//     // text = text.replace(/(?<!href=")(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>');
//     text = text.replace(/(^|[^">])(https?:\/\/[^\s)]+)/g, '$1<a href="$2" target="_blank">$2</a>');

//     // Ensure line breaks are handled properly
//     text = text.replace(/\n/g, "<br>");

//     messageDiv.innerHTML = text.trim(); // Ensures proper formatting
//     chatBody.appendChild(messageDiv);
//     chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to latest message
// }



// Function to display messages in chat
// function displayMessage(text, className) {
//     var chatBody = document.getElementById("chat-body");
//     var messageDiv = document.createElement("div");
//     messageDiv.classList.add("chat-message", className);
//     messageDiv.innerHTML = text;  // ✅ Ensures HTML tags render correctly
//     chatBody.appendChild(messageDiv);
//     chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to latest message
// }

// this functuion uses Showdown method and easy which is good but sometime links wont be clickable
// function displayMessage(text, className) {
//     var chatBody = document.getElementById("chat-body");
//     var messageDiv = document.createElement("div");
//     messageDiv.classList.add("chat-message", className);

//     // Convert Markdown to HTML using Showdown
//     var converter = new showdown.Converter();
//     text = converter.makeHtml(text);

//     // Ensure all links open in a new tab
//     text = text.replace(/<a href="(.*?)"/g, '<a href="$1" target="_blank" rel="noopener noreferrer"');

//     // Ensure line breaks are handled properly
//     text = text.replace(/\n/g, "<br>");

//     messageDiv.innerHTML = text.trim(); // Ensures text doesn't start with extra spaces
//     chatBody.appendChild(messageDiv);
//     chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to latest message
// }



// in this function im using regex to ensure the links are clickable-above function is good without this
// function displayMessage(text, className) {
//     var chatBody = document.getElementById("chat-body");
//     var messageDiv = document.createElement("div");
//     messageDiv.classList.add("chat-message", className);

//     // Convert **bold** to <b>bold</b>
//     text = text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");

//     // Convert [text](URL) Markdown-style links to proper clickable links
//     text = text.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

//     // Convert raw URLs into clickable links (but avoid capturing extra parentheses)
//     //text = text.replace(/(https?:\/\/[^\s)]+)/g, '<a href="$1" target="_blank">$1</a>');
    
//     // Convert Markdown [text](URL) links to proper clickable links
//     text = text.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g, '<a href="$2" target="_blank">$1</a>');

//     // Convert raw URLs into clickable links, but avoid links that are already inside <a> tags
//     text = text.replace(/(^|[^">])(https?:\/\/[^\s)]+)/g, '$1<a href="$2" target="_blank">$2</a>');


//     // Convert bullet points (*) or (-) into HTML lists
//     text = text.replace(/(?:^|\n)[*-]\s+(.*?)(?=\n|$)/g, "<li>$1</li>");
//     text = text.replace(/(<li>.*?<\/li>)+/g, "<ul>$&</ul>");  // Wrap <li> in <ul>

//     // Ensure line breaks are converted to <br> but not inside links
//     text = text.replace(/\n(?!<\/?a>)/g, " "); // Prevents breaking inside links

//     messageDiv.innerHTML = text.trim(); // Ensures text doesn't start with extra spaces
//     chatBody.appendChild(messageDiv);
//     chatBody.scrollTop = chatBody.scrollHeight; // Auto-scroll to latest message
// }


  



