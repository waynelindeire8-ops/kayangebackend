import os
import time

try:  # load a local .env file if python-dotenv is installed (dev convenience)
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Set Malawi time (CAT, UTC+2) for all datetime.now() / date.today() calls
os.environ['TZ'] = 'Africa/Blantyre'
try:
    time.tzset()
except AttributeError:
    pass  # Windows compat

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def _required(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable {name}. "
            "Copy .env.example to .env (local) or set it in your host's dashboard."
        )
    return value


def _flag(name, default):
    return os.environ.get(name, str(default)).strip().lower() in ('1', 'true', 'yes', 'on')


_IS_CLOUD = bool(os.environ.get('VERCEL') or os.environ.get('RENDER') or os.environ.get('FLY_APP_NAME')
                 or os.environ.get('ENVIRONMENT') == 'production')


class Config:
    # --- secrets: no defaults on purpose; the app refuses to start without them ---
    SECRET_KEY = _required('SECRET_KEY')
    JWT_SECRET_KEY = _required('JWT_SECRET_KEY')

    JWT_ACCESS_TOKEN_EXPIRES = 36000
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_NAME = 'access_token'

    # --- cookie / CORS settings for the split frontend + API ---
    # Production (HTTPS): COOKIE_SECURE=1. Local http://localhost dev: COOKIE_SECURE=0.
    COOKIE_SECURE = _flag('COOKIE_SECURE', _IS_CLOUD)
    # 'Lax' works when frontend and API are subdomains of one domain (app.x.com / api.x.com).
    # Use 'None' (requires COOKIE_SECURE=1) if they are on unrelated domains.
    COOKIE_SAMESITE = os.environ.get('COOKIE_SAMESITE', 'Lax')
    COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN') or None
    JWT_COOKIE_SECURE = COOKIE_SECURE
    JWT_COOKIE_SAMESITE = COOKIE_SAMESITE
    JWT_COOKIE_DOMAIN = COOKIE_DOMAIN

    # Comma-separated list of origins allowed to call this API, e.g.
    # FRONTEND_ORIGINS=https://app.yourdomain.com,http://localhost:8788
    FRONTEND_ORIGINS = [o.strip() for o in os.environ.get('FRONTEND_ORIGINS', '').split(',') if o.strip()]

    CALL_OUT_FEE = 20000
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads/patient_documents')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024

    DATABASE = os.environ.get('DATABASE_PATH') or ('/tmp/kayange.db' if _IS_CLOUD else os.path.join(BASE_DIR, 'kayange.db'))

    DEBUG = not _IS_CLOUD

    # --- Supabase (optional until you move fully to Postgres) ---
    SUPABASE_URL = os.environ.get('SUPABASE_URL', '')
    SUPABASE_KEY = os.environ.get('SUPABASE_KEY', '')
    SUPABASE_DB_URL = os.environ.get('SUPABASE_DB_URL', '')
    SUPABASE_DB_HOST = os.environ.get('SUPABASE_DB_HOST', '')
    SUPABASE_DB_PORT = os.environ.get('SUPABASE_DB_PORT', '6543')
    SUPABASE_DB_USER = os.environ.get('SUPABASE_DB_USER', '')
    SUPABASE_DB_PASSWORD = os.environ.get('SUPABASE_DB_PASSWORD', '')

    # --- OneDrive / Microsoft Graph backups (optional) ---
    ONEDRIVE_CLIENT_ID = os.environ.get('ONEDRIVE_CLIENT_ID', '')
    ONEDRIVE_CLIENT_SECRET = os.environ.get('ONEDRIVE_CLIENT_SECRET', '')
    ONEDRIVE_TENANT_ID = os.environ.get('ONEDRIVE_TENANT_ID', 'common')
    ONEDRIVE_REFRESH_TOKEN = os.environ.get('ONEDRIVE_REFRESH_TOKEN', '')
    ONEDRIVE_USER_EMAIL = os.environ.get('ONEDRIVE_USER_EMAIL', '')
    ONEDRIVE_BACKUP_FOLDER = os.environ.get('ONEDRIVE_BACKUP_FOLDER', '/Kayange Clinic Backups')
