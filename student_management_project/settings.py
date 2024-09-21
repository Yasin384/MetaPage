


from pathlib import Path
import os
import dj_database_url

# Определите базовый путь вашего проекта
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"  # Это для collectstatic
STATICFILES_DIRS = [
     # Убедитесь, что эта директория действительно существует
]


# Логгирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# SECURITY WARNING: храните секретный ключ в производственной среде в секрете!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'your-default-dev-secret-key')

# Debugging - отключено в производственной среде
DEBUG = True

# Разрешенные хосты
ALLOWED_HOSTS = [
    'web-production-e8c3.up.railway.app',  # Railway production host
    '127.0.0.1',
    'localhost',
    "*",
]

# Определение приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'student_management',
    'rest_framework',
    'django_extensions',
    'sslserver',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Для обработки статических файлов в производственной среде
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Хранение статических файлов
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'student_management_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'student_management_project.wsgi.application'

# Настройка базы данных
if 'DATABASE_URL' in os.environ:
    # Для производства (PostgreSQL на Railway)
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
    }
else:
    # По умолчанию SQLite для разработки
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Настройки Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'amqp://guest:guest@localhost:5672//')
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_BEAT_SCHEDULE = {
    'check-attendance': {
        'task': 'student_management.tasks.check_attendance',
        'schedule': '*/1 * * * *',  # Каждую минуту
    },
}
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Настройки аутентификации
AUTH_USER_MODEL = 'student_management.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LOGIN_URL = '/login/'  # Настройте это в зависимости от вашего URL для входа

# Проверка паролей
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

# Интернационализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Настройки безопасности и CSRF
CSRF_TRUSTED_ORIGINS = [
    'https://web-production-e8c3.up.railway.app'
]

# Настройки безопасности (настраивайте для производства позже)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Куда отправляется переадресация SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Тип поля основного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
