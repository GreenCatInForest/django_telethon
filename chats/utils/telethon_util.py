from telethon import TelegramClient
from decouple import config
import os

# Load API credentials from .env
API_ID = config('TELEGRAM_API_ID', default='')
API_HASH = config('TELEGRAM_API_HASH', default='')

# Storing session files in a secure subdirectory
SESSION_DIR = os.path.join(os.path.dirname(__file__), 'sessions')
os.makedirs(SESSION_DIR, exist_ok=True)

# get_telegram_client returns a configured TelegramClient object
def get_telegram_client(session_name='anon'):
    session_path = os.path.join(SESSION_DIR, session_name)
    return TelegramClient(session_path, API_ID, API_HASH)