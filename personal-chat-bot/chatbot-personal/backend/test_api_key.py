"""Test script to verify OpenAI API key is loaded correctly in Django settings"""
import os
import sys
import django
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.conf import settings

print("=" * 60)
print("Testing OpenAI API Key Loading")
print("=" * 60)
print(f"BASE_DIR: {settings.BASE_DIR}")
print(f"BASE_DIR.parent: {settings.BASE_DIR.parent}")
print(f"\nLooking for .env files:")
env_file1 = settings.BASE_DIR.parent / '.env'
env_file2 = settings.BASE_DIR / '.env'
print(f"  - {env_file1}: {env_file1.exists()}")
print(f"  - {env_file2}: {env_file2.exists()}")

if env_file1.exists():
    print(f"\nReading .env file directly from: {env_file1}")
    try:
        with open(env_file1, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('OPENAI_API_KEY='):
                    value = line.split('=', 1)[1].strip().strip('"').strip("'")
                    print(f"  Found in file: {value[:20]}... (length: {len(value)})")
                    break
    except Exception as e:
        print(f"  Error reading file: {e}")

print(f"\nOPENAI_API_KEY from settings:")
api_key = settings.OPENAI_API_KEY
if api_key:
    print(f"  [OK] API Key is loaded!")
    print(f"  [OK] Length: {len(api_key)}")
    print(f"  [OK] Starts with: {api_key[:20]}...")
else:
    print(f"  [ERROR] API Key is NOT loaded!")
    print(f"  [ERROR] Value: {repr(api_key)}")

# Also check environment directly
print(f"\nOPENAI_API_KEY from os.getenv:")
env_key = os.getenv('OPENAI_API_KEY', '')
if env_key:
    print(f"  [OK] API Key found in environment!")
    print(f"  [OK] Length: {len(env_key)}")
    print(f"  [OK] Starts with: {env_key[:20]}...")
else:
    print(f"  [ERROR] API Key NOT found in environment!")

print("=" * 60)


