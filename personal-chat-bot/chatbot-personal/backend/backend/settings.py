"""
Django settings for backend project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
# Try parent directory first (chatbot-personal/.env), then backend directory
env_paths = [
    BASE_DIR.parent / '.env',  # chatbot-personal/.env
    BASE_DIR / '.env',         # backend/.env (fallback)
]

print(f"[ENV] Checking environment file paths...")
print(f"[ENV] BASE_DIR: {BASE_DIR}")

env_loaded = False
for env_path in env_paths:
    print(f"[ENV] Checking path: {env_path}")
    if env_path.exists():
        print(f"[ENV] ✓ Found .env file at: {env_path}")
        load_dotenv(dotenv_path=env_path, override=True)
        env_loaded = True
        print(f"[ENV] ✓ Successfully loaded .env from: {env_path}")
        break
    else:
        print(f"[ENV] ✗ File not found at: {env_path}")

# Fallback: try loading from current directory
if not env_loaded:
    print(f"[ENV] No .env file found in specified paths, trying current directory...")
    result = load_dotenv()
    if result:
        print(f"[ENV] ✓ Loaded .env from current directory")
    else:
        print(f"[ENV] ✗ No .env file found anywhere")

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dev-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'assistant',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database - PostgreSQL ONLY
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'ai_assistant'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', '2015'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# OpenAI API Key - try multiple methods to load
print(f"[ENV] Checking for OPENAI_API_KEY...")
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
if OPENAI_API_KEY:
    print(f"[ENV] ✓ OPENAI_API_KEY found in environment variables")
else:
    print(f"[ENV] ✗ OPENAI_API_KEY not found in environment, trying to reload...")
    # Try loading again with explicit paths (parent directory first)
    for env_file in [BASE_DIR.parent / '.env', BASE_DIR / '.env']:
        if env_file.exists():
            print(f"[ENV] Attempting to reload .env from: {env_file}")
            load_dotenv(dotenv_path=env_file, override=True)
            OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
            if OPENAI_API_KEY:
                print(f"[ENV] ✓ OPENAI_API_KEY loaded from: {env_file}")
                break
        
# If still not found, try reading directly from file as fallback
if not OPENAI_API_KEY:
    print(f"[ENV] Trying to read OPENAI_API_KEY directly from file...")
    for env_file in [BASE_DIR.parent / '.env', BASE_DIR / '.env']:
        if env_file.exists():
            try:
                print(f"[ENV] Reading .env file directly: {env_file}")
                with open(env_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    print(f"[ENV] Found {len(lines)} lines in .env file")
                    for line_num, line in enumerate(lines, 1):
                        original_line = line
                        line = line.strip()
                        # Skip empty lines and comments
                        if not line or line.startswith('#'):
                            continue
                        if 'OPENAI_API_KEY' in line:
                            print(f"[ENV] Found OPENAI_API_KEY on line {line_num}: {line[:50]}...")
                            if '=' in line:
                                key_value = line.split('=', 1)
                                if len(key_value) == 2:
                                    OPENAI_API_KEY = key_value[1].strip().strip('"').strip("'")
                                    # Also set it in os.environ so other parts of the app can access it
                                    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
                                    print(f"[ENV] ✓ OPENAI_API_KEY loaded directly from file (length: {len(OPENAI_API_KEY)})")
                                    break
                    if OPENAI_API_KEY:
                        break
            except Exception as e:
                import sys
                print(f"[ENV] ✗ Warning: Could not read .env file directly: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()

if not OPENAI_API_KEY:
    print(f"[ENV] ⚠ WARNING: OPENAI_API_KEY is not set!")
else:
    print(f"[ENV] ✓ OPENAI_API_KEY is configured")

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

