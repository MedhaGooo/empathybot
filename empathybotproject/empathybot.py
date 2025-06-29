# empathybot.py

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from flask import Flask, request, jsonify
import streamlit as st
import threading
import requests
import random
import time

# ========== Load DialoGPT model ==========
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")

# Store user chat histories
chat_histories = {}

# Offensive words list
OFFENSIVE_WORDS = ["hate", "stupid", "kill", "dumb", "useless"]

# Empathetic fallback lines
EMPATHY_LINES = [
    "I'm here for you. You're not alone.",
    "It’s okay to feel this way. Let’s talk it through.",
    "You're strong for reaching out. How can I help you today?",
    "No matter what you're going through, I’m listening. 💛"
]

# ========== Functions ==========

def contains_offensive(text):
    return any(word in text.lower() for word in OFFENSIVE_WORDS)

def get_empathy_line():
    return random.choice(EMPATHY_LINES)

def generate_response(user_input, history=None):
    input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
    bot_input_ids = torch.cat([history, input_ids], dim=-1) if history is not None else input_ids
    chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

# ========== Flask Backend ==========

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    user_id = request.json.get("user_id", "anonymous")

    if contains_offensive(user_input):
        return jsonify({"response": "Let's keep this conversation respectful and kind 💛"})

    history = chat_histories.get(user_id)
    response, new_history = generate_response(user_input, history)
    chat_histories[user_id] = new_history

    with open("session_log.txt", "a") as log:
        log.write(f"{user_id}: {user_input} -> {response}\n")

    return jsonify({"response": response if response else get_empathy_line()})

# ========== Start Flask in a Thread ==========

def run_flask():
    app.run(debug=False)

flask_thread = threading.Thread(target=run_flask)
flask_thread.daemon = True
flask_thread.start()
time.sleep(1)  # Give Flask time to start

# ========== Streamlit UI Frontend ==========

st.set_page_config(page_title="EmpathyBot", page_icon="💬", layout="centered")
st.title("💬 EmpathyBot: Your Mental Health Companion")
st.markdown("_A safe space to express and talk._")

user_id = "user123"
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []

user_input = st.text_input("You:", key="input")
if st.button("Send") and user_input:
    st.session_state.chat_log.append(f"You: {user_input}")
    try:
        response = requests.post("http://127.0.0.1:5000/chat", json={"message": user_input, "user_id": user_id}).json()["response"]
    except Exception:
        response = "⚠️ Could not connect to chatbot backend. Please try again."
    st.session_state.chat_log.append(f"EmpathyBot: {response}")

for msg in st.session_state.chat_log:
    st.markdown(msg)
