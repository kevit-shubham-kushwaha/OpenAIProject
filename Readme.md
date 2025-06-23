# 🚀 OpenAIProject

A simple OpenAI backend project built with **FastAPI**.

## 📌 Overview

This project serves as the initial setup for building scalable APIs using FastAPI. It currently includes a basic health check and index route.

## 🛠️ Tech Stack

- **FastAPI** – High-performance web framework
- **Uvicorn** – ASGI server (used internally by FastAPI)

## 📂 Current Routes

- `GET /` – Index route  
- `GET /health` – Health check endpoint  

## ▶️ How to Run

Make sure you have Python 3.12+ installed.

### 1️⃣ Create and Activate Virtual Environment

#### macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate

python -m venv venv
venv\Scripts\activate

### 1️⃣ Install dependencies

```bash
pip install -r requirements.txt
