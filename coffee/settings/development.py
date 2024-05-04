from .base import *

# Debug Config
DEBUG =  config("DEBUG", default=True, cast=bool)

# Allowed Hosts Config
ALLOWED_HOSTS = []

# Data Base config

ALTERNATIVE_DBS = {
    "postgres": {
        "ENGINE": config("ENGINE",default="django.db.backends.postgresql"),
        "NAME": config("DB_NAME", default="django_template"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="127.0.0.1"),
        "PORT": config("DB_PORT", default=5432),
    },
    
    'sqlite3': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = {
    "default": ALTERNATIVE_DBS[config("USERDB", default="postgres")],
}

# Static media file config
STATIC_URL = 'static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# Configure cors origin 
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost",
]

CORS_ORIGIN_WHITELIST =[
    "http://localhost:3000",
    "http://localhost",  
]
