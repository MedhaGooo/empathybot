# 🤖 EmpathyBot: A Mental Health Support Chatbot

Welcome to **EmpathyBot** — a compassionate AI chatbot built to provide emotional support and a listening ear. It's not just code — it's an effort to bring kindness, empathy, and understanding into our digital spaces.

---

## 🌱 About This Project

“Sometimes, just being heard is enough.” — Unknown

Mental health matters, and sometimes just having someone (or something) to talk to can make a difference. **EmpathyBot** is a lightweight, Python-based chatbot that simulates friendly, non-judgmental conversations. It uses a fine-tuned conversational AI model to offer comfort, encouragement, and a safe space to share.

This project is ideal for:
- Students exploring AI and mental health applications
- Beginners learning Flask + Streamlit
- Hackathon prototypes or research demos

---

## 🧠 Features

- 🤗 Powered by [DialoGPT](https://huggingface.co/microsoft/DialoGPT-small) from Hugging Face
- 🛡️ Filters offensive or inappropriate inputs
- 💬 Includes pre-written empathetic responses when the AI doesn’t know what to say
- 📊 Logs user chat sessions for analysis or improvement
- 🌐 Runs with Flask (API) and Streamlit (UI) in a single file
- 🐍 100% Python — no need for HTML, JavaScript, or CSS

---

## 💻 How to Run EmpathyBot

### 🔧 1. Install Dependencies

Make sure you have Python installed, then run:
streamlit run empathybot.py

```bash
pip install -r requirements.txt

empathybot/
│
├── empathybot.py        # Main chatbot code (Flask + Streamlit)
├── requirements.txt     # List of Python dependencies
├── session_log.txt      # (Optional) Logs of user chats
└── README.md            # You’re reading this 🙂

