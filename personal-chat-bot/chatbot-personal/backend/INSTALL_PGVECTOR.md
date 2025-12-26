# How to Install pgvector in PostgreSQL (Windows)

This guide will help you install the pgvector extension in your PostgreSQL database.

## Method 1: Try SQL Command First (Easiest - if extension is pre-installed)

If your PostgreSQL installation already has pgvector available, you just need to enable it:

1. **Connect to PostgreSQL** using one of these methods:
   - **pgAdmin**: Open pgAdmin → Right-click your database (`ai_assistant`) → Query Tool
   - **psql**: Open Command Prompt/PowerShell and run:
     ```bash
     psql -U postgres -d ai_assistant
     ```
   - **Any SQL client**: Connect to your database

2. **Run this SQL command**:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```

3. **Verify it's installed**:
   ```sql
   SELECT * FROM pg_extension WHERE extname = 'vector';
   ```

If this works, you're done! If you get an error saying the extension doesn't exist, continue to Method 2.

---

## Method 2: Download Pre-built Binaries (Easiest for Windows)

### Step 1: Find Your PostgreSQL Version

1. Open **psql** or **pgAdmin**
2. Run this command:
   ```sql
   SELECT version();
   ```
   Note your PostgreSQL version number (e.g., 15, 16, etc.)

### Step 2: Download Pre-built pgvector

1. Go to: **https://github.com/pgvector/pgvector/releases**
2. Scroll down to find **Assets** section for the latest release
3. Look for Windows binaries. You may see:
   - Pre-built DLL files for different PostgreSQL versions
   - OR you might need to build from source (see Method 3)

**If pre-built binaries are available:**
- Download the zip file matching your PostgreSQL version
- Extract it

**If pre-built binaries are NOT available**, you'll need to build from source (see Method 3 below).

### Step 3: Find Your PostgreSQL Installation Directory

Common locations:
- `C:\Program Files\PostgreSQL\15\` (or 14, 16, etc.)
- `C:\Program Files (x86)\PostgreSQL\15\`

To find it:
1. Open **Services** (Win + R → `services.msc`)
2. Find your PostgreSQL service (e.g., `postgresql-x64-15`)
3. Right-click → Properties → Check the path

### Step 4: Copy Files

1. **Copy the DLL file**:
   - Find `vector.dll` in the extracted files
   - Copy to: `[PostgreSQL Installation]\lib\`
   - Example: `C:\Program Files\PostgreSQL\15\lib\vector.dll`

2. **Copy the SQL files**:
   - Find `vector.control` and `vector--*.sql` files
   - Copy to: `[PostgreSQL Installation]\share\extension\`
   - Example: `C:\Program Files\PostgreSQL\15\share\extension\`

### Step 5: Restart PostgreSQL Service

1. Open **Services** (Win + R → `services.msc`)
2. Find your PostgreSQL service
3. Right-click → **Restart**

OR PowerShell (as Administrator):
```powershell
Restart-Service postgresql-x64-15
```
(Replace `15` with your version)

### Step 6: Enable the Extension

1. Connect to PostgreSQL (pgAdmin, psql, or any SQL client)
2. Connect to your `ai_assistant` database
3. Run:
   ```sql
   CREATE EXTENSION vector;
   ```

### Step 7: Verify Installation

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

---

## Method 3: Build from Source (If pre-built binaries unavailable)

If you can't find pre-built binaries, you can build pgvector from source:

### Prerequisites:
1. **Visual Studio Build Tools** (download from Microsoft)
2. **Git** (to clone the repository)

### Steps:

1. **Install Visual Studio Build Tools**:
   - Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "Desktop development with C++" workload

2. **Clone pgvector repository**:
   ```cmd
   git clone --branch v0.8.1 https://github.com/pgvector/pgvector.git
   cd pgvector
   ```

3. **Set up build environment** (in Developer Command Prompt):
   ```cmd
   "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"
   ```
   (Adjust path to your Visual Studio installation)

4. **Build and install**:
   ```cmd
   set "PGROOT=C:\Program Files\PostgreSQL\16"
   nmake /F Makefile.win
   nmake /F Makefile.win install
   ```
   (Replace `16` with your PostgreSQL version)

5. **Restart PostgreSQL service**

6. **Enable extension**:
   ```sql
   CREATE EXTENSION vector;
   ```

---

## Method 3: Using Docker (Alternative - if you want to start fresh)

If you prefer using Docker instead:

1. **Stop your current PostgreSQL** (if running)

2. **Run this Docker command**:
   ```bash
   docker run -d --name postgres-pgvector -e POSTGRES_PASSWORD=2015 -e POSTGRES_DB=ai_assistant -p 5432:5432 pgvector/pgvector:pg16
   ```

3. **Update your .env file** if needed (usually stays the same)

4. **Enable extension** (connect and run):
   ```sql
   CREATE EXTENSION vector;
   ```

---

## Quick Check Script

After installation, you can verify using our check script:

```bash
cd personal-chat-bot\chatbot-personal\backend
python check_pgvector.py
```

This will tell you if pgvector is available and installed.

---

## Troubleshooting

### Error: "extension vector does not exist"
- The extension files are not installed correctly
- Make sure you copied the DLL and SQL files to the correct directories
- Restart PostgreSQL service after copying files

### Error: "permission denied"
- Run psql/pgAdmin as Administrator
- Or use a superuser account (like `postgres`)

### Error: "could not load library"
- The DLL version doesn't match your PostgreSQL version
- Make sure you downloaded the correct version
- Check that the DLL is in the `lib` directory

### Can't find PostgreSQL installation directory
- Check Services → postgresql service → Properties → Path to executable
- Or check Program Files/Program Files (x86) for PostgreSQL folders

---

## Notes

- **You don't need pgvector for the current setup to work** - the Python-based cosine similarity works fine
- pgvector provides better performance for large datasets
- The current implementation stores vectors as JSON strings and works without pgvector
- Installing pgvector is optional but recommended for production use

