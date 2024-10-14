from .base import *

# Debug Config
DEBUG =  config("DEBUG", default=False, cast=bool)

# Allowed Hosts Config
ALLOWED_HOSTS = ["*"]

# Data Base config
DATABASES = {
    "default": {
        "ENGINE": config("ENGINE",default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="django_template"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="127.0.0.1"),
        "PORT": config("DB_PORT", default=5432),
    }
}

ROOT_URLCONF = 'coffee.urls'

# Static media file config
STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [
    BASE_DIR / "static",
]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configure cors origin 
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",
]

CORS_ORIGIN_WHITELIST =[
    "http://localhost:3000",
    "http://localhost",  
]