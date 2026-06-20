const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false;
recognition.interimResults = false;

async function startMS() {
    const circle = document.getElementById("circle");
    const text = document.getElementById("text");
    const status = document.getElementById("status");
    
    circle.classList.add("listening");
    text.innerText = "Listening...";
    status.innerText = "Active";
    
    recognition.start();

    // Jab user bolna band kare
    recognition.onspeechend = () => {
        recognition.stop();
        status.innerText = "Thinking...";
    };

    recognition.onresult = async (event) => {
        const userText = event.results[0][0].transcript;
        text.innerText = "Processing...";
        
        try {
            const res = await fetch("/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userText })
            });
            const data = await res.json();
            
            text.innerText = data.reply;
            status.innerText = "Ready";
            circle.classList.remove("listening"); // UI reset
        } catch (err) {
            text.innerText = "Server Error";
            status.innerText = "Error";
            circle.classList.remove("listening");
        }
    };

    recognition.onerror = () => {
        circle.classList.remove("listening");
        text.innerText = "Tap to try again";
        status.innerText = "Ready";
    };
}

async function clearMSMemory() {
    const text = document.getElementById("text");
    const circle = document.getElementById("circle");
    const status = document.getElementById("status");

    try {
        const res = await fetch("/clear", { method: "POST" });
        const data = await res.json();
        
        // Memory clear hone ka text screen par dikhayega
        text.innerText = data.reply; 
        circle.classList.remove("listening"); // Safety check
        status.innerText = "Cleared";
        
        // 4 second baad UI reset
        setTimeout(() => {
            text.innerText = "Tap to Speak";
            status.innerText = "Ready";
        }, 4000);
    } catch (err) {
        console.error("Clear memory error:", err);
        text.innerText = "Reset Failed";
    }
}