"""
Quick script to check if pgvector extension is available in PostgreSQL
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.db import connection

try:
    with connection.cursor() as cursor:
        # Check if pgvector extension exists
        cursor.execute("""
            SELECT EXISTS(
                SELECT 1 FROM pg_available_extensions 
                WHERE name = 'vector'
            );
        """)
        available = cursor.fetchone()[0]
        
        if available:
            print("[OK] pgvector extension is AVAILABLE in PostgreSQL")
            
            # Check if it's installed
            cursor.execute("""
                SELECT EXISTS(
                    SELECT 1 FROM pg_extension 
                    WHERE extname = 'vector'
                );
            """)
            installed = cursor.fetchone()[0]
            
            if installed:
                print("[OK] pgvector extension is INSTALLED in the database")
            else:
                print("[WARNING] pgvector extension is available but NOT installed")
                print("  You can install it by running: CREATE EXTENSION vector;")
        else:
            print("[ERROR] pgvector extension is NOT AVAILABLE")
            print("  You need to install pgvector on your PostgreSQL server first.")
            print("  See PGVECTOR_SETUP.md for instructions.")
            
except Exception as e:
    print(f"Error checking pgvector: {e}")
    print("\nThis might indicate:")
    print("1. PostgreSQL connection issue")
    print("2. Database doesn't exist")
    print("3. User doesn't have permission to check extensions")

