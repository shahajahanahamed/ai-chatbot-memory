# 🧠 AI Chatbot with Memory (FastAPI + Redis)

A backend AI chatbot built with FastAPI that supports **multi-turn conversations using Redis-based memory**.

This project demonstrates how to build a **stateful AI system** on top of stateless LLMs using clean architecture and scalable design patterns.

---

# 🚀 Project Overview

Large Language Models (LLMs) are **stateless by default** — they do not remember previous messages.

This project solves that problem by introducing:

- ✅ Session-based memory using Redis  
- ✅ Multi-turn conversation support  
- ✅ Clean backend architecture (API → Service → Provider → Memory)  
- ✅ Extensible LLM provider system (Groq / OpenAI)

---

# ✨ Features

## Core Features
- FastAPI REST API
- LLM integration via provider pattern
- Structured logging
- Clean modular architecture

## Memory Features (Redis)
- Conversation history stored in Redis
- Per-user + per-session isolation
- Auto-expiry using TTL
- Message trimming to avoid overflow

## Session Support
- Multiple sessions per user
- Independent chat context per session

---

# 🏗️ Project Structure
```aiignore
app/
│
├── api/
│ └── v1/
│ └── endpoint.py # API routes (chat endpoints)
│
├── core/
│ ├── config.py # Environment configuration
│ └── logging_config.py # Logging setup
│
├── db/
│ └── redis_client.py # Redis connection setup
│
├── factory/
│ └── factory.py # LLM provider factory
│
├── provider/
│ ├── llm_provider.py # Abstract base provider
│ ├── groq_provider.py # Groq implementation
│ └── openai_provider.py # OpenAI implementation
│
├── schemas/
│ └── chat_schema.py # Request/response models
│
├── services/
│ ├── chat_service.py # Business logic
│ └── memory_service.py # Redis memory handling
│
└── main.py # FastAPI app entry point
```


---

# ⚙️ Prerequisites

Before running this project, ensure you have:

- Python 3.10+
- Redis installed or Docker installed
- Groq API key (or OpenAI API key)

---

# 🧰 Setup Guide (Step-by-Step)

## 1️⃣ Clone the Repository

```bash
git clone <your-repository-url>
cd ai-chatbot-memory
```
## 2️⃣ Create Virtual Environment
### Windows
```
python -m venv .venv
.venv\Scripts\activate
```
### Linux / Mac
```
python -m venv .venv
source .venv/bin/activate
```

## 3️⃣ Install Dependencies (Using pyproject.toml)

### This project uses pyproject.toml (PEP 517/518 standard).

If you're using pip:
```
python -m venv .venv
.venv\Scripts\activate
```

Or for development:
```
pip install -e .
```
## 4️⃣ Configure Environment Variables

#### Create a .env file in the root directory:

```
APP_NAME=AI Chatbot
APP_VERSION=0.0.1

DEBUG=true
LOG_LEVEL=DEBUG

LLM_PROVIDER=groq

GROQ_API_KEY=your_api_key_here
GROQ_MODEL=llama-3.1-8b-instant

LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1000
```

⚠️ Important: Never commit .env to Git.


## 🔴 Redis Setup (Required)

#### This project uses Redis for storing conversation memory.

### Option 1: Using Docker (Recommended)
```
docker run -d -p 6379:6379 redis:7
```
### Option 2: Local Installation

##### Ensure Redis is running at:

```
localhost:6379
```
#### Verify Redis
```
redis-cli ping
```

#### Expected output:

```
PONG
```
## ▶️ Running the Application

### Start the FastAPI server:

```
uvicorn app.main:app --reload
```
### Access API Docs

Open in browser:

```
http://127.0.0.1:8000/docs
```

## 📡 API Usage
### 🔹 Chat Endpoint

POST /api/v1/chat

#### Request Body
```
{
  "query": "Hello",
  "user_id": 1,
  "session_id": "session1"
}
```
### 🔹 Clear Chat

DELETE /api/v1/chat/{user_id}/{session_id}

## 🧠 How Memory Works

##### Each conversation is stored in Redis using a key:

``` 
chat:{user_id}:{session_id}
```
#### Example:
```
chat:1:session1
```

### Memory Behavior
- Stores messages as JSON
- Maintains conversation history
- Automatically expires after TTL (1 hour)
- Keeps only recent messages (to prevent token overflow)

## 📊 Logging
- Configurable via .env
- Includes:
    - user_id
    - session_id
    - request lifecycle
- Useful for debugging and monitoring

## ⚠️ Limitations
- Memory is not persistent (Redis only)
- No authentication (user_id passed manually)
- No streaming responses
- No database storage

## 🚀 Future Improvements
  - PostgreSQL for persistent chat storage
  - WebSocket streaming responses
  - JWT authentication
  - Rate limiting
  - Multi-model routing

## 👨‍💻 Author

    Reeju
    Java Full Stack Developer exploring AI backend systems

## 📜 License

    This project is for learning and demonstration purposes.
