"""
EcoMboa — Production Settings
-------------------------------
Full security hardening for Railway / Render deployment.
All secrets MUST be provided as environment variables.
"""
from .base import *  # noqa: F401, F403
from decouple import config
import dj_database_url  # type: ignore

# ─────────────────────────────────────────────────────────────────────────────
# CORE
# ─────────────────────────────────────────────────────────────────────────────
DEBUG = False

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# ─────────────────────────────────────────────────────────────────────────────
# DATABASE — PostgreSQL with SSL in production
# ─────────────────────────────────────────────────────────────────────────────
DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True,
    )
}

# ─────────────────────────────────────────────────────────────────────────────
# SECURITY HEADERS — maximum hardening
# ─────────────────────────────────────────────────────────────────────────────
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# HSTS
SECURE_HSTS_SECONDS = 31536000         # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Cookie security
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Content security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# ─────────────────────────────────────────────────────────────────────────────
# EMAIL — SMTP in production
# ─────────────────────────────────────────────────────────────────────────────
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# ─────────────────────────────────────────────────────────────────────────────
# ALLAUTH — mandatory email verification in production
# ─────────────────────────────────────────────────────────────────────────────
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# ─────────────────────────────────────────────────────────────────────────────
# MEDIA — Cloudinary only in production (already set in base.py)
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ─────────────────────────────────────────────────────────────────────────────
# STATIC — WhiteNoise for serving static files from Railway/Render
# ─────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
] + MIDDLEWARE[1:]  # noqa: F405

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ─────────────────────────────────────────────────────────────────────────────
# CHANNELS — Redis in production (base.py already reads REDIS_URL)
# ─────────────────────────────────────────────────────────────────────────────
# CHANNEL_LAYERS from base.py is correct for production.

# ─────────────────────────────────────────────────────────────────────────────
# CORS — restrict to known domain
# ─────────────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://ecomboa.cm',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ─────────────────────────────────────────────────────────────────────────────
# LOGGING — file logging in production
# ─────────────────────────────────────────────────────────────────────────────
LOGGING['handlers']['console']['level'] = 'WARNING'  # noqa: F405
