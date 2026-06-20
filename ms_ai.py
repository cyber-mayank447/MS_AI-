import pyttsx3
import threading
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
from groq import Groq
import webbrowser
import smtplib
from email.message import EmailMessage

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

API_KEY = "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"

client = Groq(api_key=API_KEY) if API_KEY else None
chat_history = []

def speak(text):
    def run_voice():
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id) 
            engine.setProperty('rate', 150)
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"Voice Status: {e}")
    threading.Thread(target=run_voice, daemon=True).start()

def send_email(receiver, subject, content):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = "prajapatboy184@gmail.com"
        msg['To'] = receiver
        msg.set_content(content)
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("prajapatboy184@gmail.com", "tuzv gsda kwzw zrsq")
            smtp.send_message(msg)
        return True
    except: return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    global chat_history
    user_said = request.json.get("message", "").lower().strip()
    reply = ""

    # --- 1. BASIC COMMANDS ---
    if "hello ms" in user_said:
        reply = "Hii, I am M S. Mayank sir ki personal assistant."

    elif "my school director name" in user_said:
        reply = "E Planet Academy ke directors Anupam Sharma aur Manoj Sharma hain."

    # --- 2. EMAIL FEATURE ---
    elif "send email" in user_said:
        email_msg = user_said.replace("send email", "").strip() or "Hello from MS AI Project."
        status = send_email("prajapatboy184@gmail.com", "MS AI Project Update", email_msg)
        reply = "Email bhej diya gaya hai, sir." if status else "Email bhejte waqt error aaya."

    # --- 3. SYSTEM COMMANDS ---
    elif "open notepad" in user_said:
        os.system("start notepad")
        reply = "Notepad khol diya gaya hoon."

    elif "open SE shop" in user_said or "shormay shop" in user_said:
        webbrowser.open("https://www.meesho.com/ShoryamEnterprises?ms=2")
        reply = "Theek hai sir, E Planet Academy ka channel khol raha hoon."

    elif "open chrome" in user_said:
        os.system("start chrome")
        reply = "Chrome browser khol diya gaya hai."

    # --- 4. AI CHAT LOGIC ---
    else:
        try:
            messages = [{"role": "system", "content": "You are MS AI, created by Mayank Sir."}]
            messages.extend(chat_history[-5:])
            messages.append({"role": "user", "content": user_said})
            completion = client.chat.completions.create(model="llama-3.1-8b-instant", messages=messages)
            reply = completion.choices[0].message.content
            
            chat_history.append({"role": "user", "content": user_said})
            chat_history.append({"role": "assistant", "content": reply})
        except:
            reply = "Server busy hai, please try again."

    speak(reply)
    return jsonify({"reply": reply})

@app.route("/clear", methods=["POST"])
def clear_memory():
    global chat_history
    chat_history = []
    reply_msg = "Yes sir. Memory cleared."
    speak(reply_msg) 
    return jsonify({"status": "cleared", "reply": reply_msg})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)