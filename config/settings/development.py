"""
EcoMboa — Development Settings
--------------------------------
Overrides for local development. Uses SQLite by default for ease of setup.
Switch DATABASE_URL in .env to PostgreSQL when ready.
"""
from .base import *  # noqa: F401, F403
from decouple import config

# ─────────────────────────────────────────────────────────────────────────────
# DEBUG — always True in development
# ─────────────────────────────────────────────────────────────────────────────
DEBUG = True
ALLOWED_HOSTS = ['*']

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE — SQLite for quick local setup, PostgreSQL recommended
# ─────────────────────────────────────────────────────────────────────────────
DATABASE_URL = config('DATABASE_URL', default='')
USE_SQLITE = config('USE_SQLITE', default=True, cast=bool)

if DATABASE_URL and not USE_SQLITE:
    import dj_database_url  # type: ignore
    try:
        DATABASES = {
            'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
        }
    except Exception:
        # Fall back to SQLite if DATABASE_URL is malformed locally.
        pass
# else: base.py SQLite default is used

# ─────────────────────────────────────────────────────────────────────────────
# EMAIL — print to console in development
# ─────────────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ─────────────────────────────────────────────────────────────────────────────
# ALLAUTH — disable email verification in development for ease of testing
# ─────────────────────────────────────────────────────────────────────────────
ACCOUNT_EMAIL_VERIFICATION = 'none'

# ─────────────────────────────────────────────────────────────────────────────
# MEDIA — use local filesystem in development
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ─────────────────────────────────────────────────────────────────────────────
# INSTALLED APPS — add debug toolbar
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = INSTALLED_APPS + ['debug_toolbar']  # noqa: F405

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
] + MIDDLEWARE  # noqa: F405

INTERNAL_IPS = ['127.0.0.1', '::1']

# ─────────────────────────────────────────────────────────────────────────────
# CHANNELS — use in-memory layer for dev (no Redis required)
# ─────────────────────────────────────────────────────────────────────────────
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer',
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING — verbose in development
# ─────────────────────────────────────────────────────────────────────────────
LOGGING['loggers']['django']['level'] = 'DEBUG'  # noqa: F405
