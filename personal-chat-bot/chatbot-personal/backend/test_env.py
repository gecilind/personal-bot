"""Test script to verify .env loading"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add the backend directory to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Load .env
env_path = BASE_DIR / '.env'
print(f"Looking for .env at: {env_path}")
print(f".env exists: {env_path.exists()}")

if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.getenv('OPENAI_API_KEY', '')
    print(f"API Key loaded: {bool(api_key)}")
    print(f"API Key length: {len(api_key) if api_key else 0}")
    if api_key:
        print(f"API Key starts with: {api_key[:10]}...")
else:
    print("ERROR: .env file not found!")

