# pgvector Extension Setup

The pgvector extension must be installed on your PostgreSQL server before running migrations.

## Installation Methods

### Option 1: Using pgvector Installation Script (Recommended for Windows)

1. Download pgvector from: https://github.com/pgvector/pgvector/releases
2. Or install using package manager if available

### Option 2: Manual Installation

For Windows PostgreSQL installations:

1. Download the appropriate pgvector DLL for your PostgreSQL version
2. Copy the DLL to your PostgreSQL `lib` directory
3. Copy the SQL files to your PostgreSQL `share/extension` directory
4. Restart PostgreSQL service

### Option 3: Using Docker (Easiest)

If you're using Docker, use a PostgreSQL image with pgvector pre-installed:

```bash
docker run -d \
  --name postgres-pgvector \
  -e POSTGRES_PASSWORD=2015 \
  -e POSTGRES_DB=ai_assistant \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

### Option 4: Manual SQL Installation

If you have admin access to PostgreSQL:

1. Connect to PostgreSQL as superuser
2. Run: `CREATE EXTENSION vector;`

## Verify Installation

After installation, verify pgvector is available:

```sql
SELECT * FROM pg_available_extensions WHERE name = 'vector';
```

If it shows up, you can proceed with migrations.

## Alternative: Skip pgvector for Now

If you cannot install pgvector immediately, you can:
1. Comment out the vector field temporarily
2. Run migrations
3. Install pgvector later
4. Add the vector field in a new migration

However, vector search functionality will not work without pgvector.

