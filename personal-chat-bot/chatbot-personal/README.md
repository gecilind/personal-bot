# Personal AI Assistant

A Django-based AI assistant powered by embeddings and vector search, trained on professional CV data with persistent memory stored in PostgreSQL.

## Features

- Django REST Framework API
- OpenAI embeddings and vector search
- PostgreSQL with pgvector extension
- Persistent memory system
- CV-based knowledge base
- Django admin interface

## Setup

### 1. Create Virtual Environment

```bash
cd chatbot-personal/backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the `backend/` directory with the following content:

```
OPENAI_API_KEY=your_actual_api_key_here
DB_NAME=ai_assistant
DB_USER=postgres
DB_PASSWORD=2015
DB_HOST=localhost
DB_PORT=5432
```

Replace `your_actual_api_key_here` with your actual OpenAI API key.

### 5. Setup PostgreSQL Database

Ensure PostgreSQL is running and create the database:

```sql
CREATE DATABASE ai_assistant;
```

### 6. Run Migrations

```bash
python manage.py migrate
```

This will create all necessary tables including the pgvector extension.

### 7. Create Superuser

```bash
python manage.py createsuperuser
```

### 8. Ingest Resume Data

```bash
python manage.py ingest_resume
```

This will read `assistant/resume.txt`, chunk it, generate embeddings, and store them in the database.

### 9. Run Development Server

```bash
python manage.py runserver
```

## Usage

- Access Django Admin: http://localhost:8000/admin/
- Chat Interface: http://localhost:8000/
- API Endpoint: http://localhost:8000/api/chat/

## API Endpoints

### POST /api/chat/

Send a message to the AI assistant.

**Request:**
```json
{
  "message": "What is your experience?"
}
```

**Response:**
```json
{
  "response": "Based on my CV, I have experience in...",
  "relevant_knowledge": [...]
}
```

### GET /api/memory/

Retrieve stored memories.

**Response:**
```json
{
  "memories": [...]
}
```

## Project Structure

```
chatbot-personal/
├── backend/
│   ├── venv/
│   ├── manage.py
│   ├── backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── ...
│   ├── assistant/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── services/
│   │   │   ├── embeddings.py
│   │   │   ├── vector_search.py
│   │   │   └── llm.py
│   │   └── ...
│   └── requirements.txt
└── README.md
```

