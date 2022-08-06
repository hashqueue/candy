"""
Django settings for candy project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
import sys
from datetime import timedelta
from pathlib import Path
from utils.django_utils.handle_config import HandleConfig

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 添加apps目录到python的里去
sys.path.insert(0, os.path.join(BASE_DIR, 'apps/'))

config = HandleConfig(file_name=os.path.join(BASE_DIR, 'config.ini'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-57cj&k#ys8k-@f6$@kfjiyii^et6p%2htwxxw8i9dkm79($vc!'
DEFAULT_USER_PASSWORD = '123456'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get_boolean_value('deploy', 'DEBUG')

ALLOWED_HOSTS = ["*"]

# Application definition

# 设置自定义的用户模型类：被Django的认证系统所识别
AUTH_USER_MODEL = 'system.User'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',
    'drf_spectacular',

    'system',
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

SPECTACULAR_SETTINGS = {
    'TITLE': 'Candy API',
    'DESCRIPTION': 'Candy权限管理系统接口文档',
    'VERSION': '1.0.0',
    'CONTACT': {"email": "1912315910@qq.com"},
    'LICENSE': {"name": "MIT License"},
    'SERVERS': [{"url": "http://127.0.0.1:8000"}],
}

API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 指定使用JWT认证
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    # 在全局指定分页的引擎
    'DEFAULT_PAGINATION_CLASS': 'utils.drf_utils.my_page_number_pagination.MyPageNumberPagination',
    # 同时必须指定每页显示的条数
    'PAGE_SIZE': 10,
    # 全局配置自定义异常
    'EXCEPTION_HANDLER': 'utils.drf_utils.custom_exception.custom_exception_handler',
    # 指定后端的schema为drf_spectacular的schema，用来生成接口文档
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES':
        [
            'rest_framework.permissions.IsAuthenticated',
            # 自定义rbac权限认证
            'utils.drf_utils.custom_permissions.RbacPermission',
        ],
    # 指定drf使用的过滤后端
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    # 接口限流
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '2000/day'
    },
    # API版本
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': API_VERSION,  # 默认的版本
    'ALLOWED_VERSIONS': [API_VERSION],  # 有效的版本
    'VERSION_PARAM': 'version',  # 版本的参数名与URL conf中一致
}

# djangorestframework-simplejwt配置
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    # 将refresh token的有效期改为2天
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
}

# url权限认证白名单
WHITE_URL_LIST = [
    f'{API_PREFIX}/swagger/', f'{API_PREFIX}/redoc/', f'{API_PREFIX}/schema/', f'{API_PREFIX}/system/user/login/',
    f'{API_PREFIX}/system/user/token/refresh/', f'{API_PREFIX}/system/user/register/',
]

AUTHENTICATION_BACKENDS = [
    # 自定义用户认证后端
    'utils.django_utils.custom_user_authentication_backend.MyCustomUserAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'candy.urls'

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

WSGI_APPLICATION = 'candy.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
# 配置图片文件上传的存储路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'media')
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# log
# 创建log文件的文件夹
LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

# django中的日志配置
LOGGING = {
    'version': 1,
    # 是否禁用已经存在的logger实例
    'disable_existing_loggers': False,
    # 日志显示格式
    'formatters': {
        # 简单格式
        'simple': {
            'format': '{asctime} - {levelname} - {message}',
            'style': '{',
        },
        # 详细格式
        'verbose': {
            'format': '{asctime} - {levelname} - {name} - [msg: {message}] - [{filename}: {lineno:d}]',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        # 只有debug=False且Error级别以上发邮件给admin
        "mail_admins": {
            "level": "ERROR",
            'filters': ['require_debug_false'],
            "class": "django.utils.log.AdminEmailHandler",
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'filters': ['require_debug_false'],
            'level': 'INFO',
            # 滚动生成日志，切割
            'class': 'logging.handlers.RotatingFileHandler',
            # 存放日志文件的位置
            'filename': os.path.join(BASE_DIR, 'logs', 'app.log'),
            'maxBytes': 100 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
    },
    'loggers': {
        # 自定义日志器，可以在代码中通过logging.getLogger("my_logger")使用
        'my_logger': {
            'handlers': ['console', 'file'],
            # 启用日志轮转机制
            'propagate': True,
            # 日志器接收的最低日志级别
            'level': 'INFO'
        },
        'django': {
            'handlers': ['mail_admins', 'file', 'console'],
            'level': 'INFO',
            'propagate': True
        },
    }
}
