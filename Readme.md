# 🚀 OpenAIProject

A FastAPI-powered backend application for building conversational assistants using OpenAI’s Chat Completion and Assistant APIs.

---

## 📌 Overview

This project lays the foundation for an AI-driven assistant system that processes user messages, classifies intent, and handles dynamic flows through OpenAI APIs.

Core features include:

- OpenAI Assistant and Chat Completion APIs integration  
- Flow detection and query classification  
- Structured logging with request tracking middleware  
- A simple HTML-based frontend at `/chats/ui`  

---

## 🛠️ Tech Stack

- **FastAPI** – High-performance Python web framework  
- **Uvicorn** – ASGI server for running FastAPI apps  
- **OpenAI API** – For assistant and completion-based responses  
- **Custom Middleware** – For logging each incoming request  
- **Logger** – File-based + console logging with structured formatting  
- **HTML + TailwindCSS** – Minimal frontend for chat interaction  

---

## 📂 Current API Endpoints

| Method | Route         | Description                              |
|--------|---------------|------------------------------------------|
| GET    | `/`           | Index route                              |
| GET    | `/health`     | Health check endpoint                    |
| POST   | `/chats/`     | Main chat handler (streaming supported)  |
| GET    | `/chats/ui`   | Frontend UI for testing assistant        |

---

## ▶️ How to Run

Make sure you have **Python 3.12+** installed.

### 🧰 Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/kevit-shubham-kushwaha/OpenAIProject.git
cd OpenAIProject

# 2. Create and activate virtual environment
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Run the application
python -m src.app

## ▶️ How to Run

Make sure you have **Python 3.12+** installed.

### 🧰 Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/kevit-shubham-kushwaha/OpenAIProject.git
cd OpenAIProject

# 2. Create and activate virtual environment
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# 3. Install project dependencies
pip install -r requirements.txt

# 4. Create and configure your .env file
cp example.env .env
# Then, open `.env` and fill in the required values like:
# OPENAI_API_KEY=your_actual_api_key
# OPENAI_MODEL_NAME=gpt-4o
# HOST=127.0.0.1
# PORT=8000

# 5. Run the application
python -m src.app
