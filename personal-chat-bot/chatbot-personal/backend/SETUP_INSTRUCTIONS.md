# Quick Setup Instructions

## Important: Create .env File

Before running the application, you **must** create a `.env` file in the `backend/` directory with the following content:

```
OPENAI_API_KEY=your_actual_openai_api_key_here
DB_NAME=ai_assistant
DB_USER=postgres
DB_PASSWORD=2015
DB_HOST=localhost
DB_PORT=5432
```

Replace `your_actual_openai_api_key_here` with your actual OpenAI API key.

## Setup Steps

1. **Create virtual environment:**
   ```bash
   cd chatbot-personal/backend
   python -m venv venv
   ```

2. **Activate virtual environment:**
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file** (see above)

5. **Create PostgreSQL database:**
   ```sql
   CREATE DATABASE ai_assistant;
   ```

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Add your CV to `assistant/resume.txt`** (paste your CV content)

9. **Ingest resume:**
   ```bash
   python manage.py ingest_resume
   ```

10. **Run server:**
    ```bash
    python manage.py runserver
    ```

## Access Points

- Chat Interface: http://localhost:8000/
- Django Admin: http://localhost:8000/admin/
- API Endpoint: http://localhost:8000/api/chat/

