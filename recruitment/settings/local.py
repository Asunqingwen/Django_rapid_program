from .base import *

DEBUG = True

ALLOWED_HOSTS = []

## 务必修改以下值，确保运行时系统安全:
SECRET_KEY = "w$46bks+b3-7f(13#i%v@jwejrnxc$^^#@#@^t@fofizy1^mo9r8(-939243423300"

# # AliCloud access key ID
# OSS_ACCESS_KEY_ID = os.environ.get('OSS_ACCESS_KEY_ID','')
# # AliCloud access key secret
# OSS_ACCESS_KEY_SECRET = os.environ.get('OSS_ACCESS_KEY_SECRET','')
# # The name of the bucket to store files in
# OSS_BUCKET_NAME = 'djangorecruit'
#
# # The URL of AliCloud OSS endpoint
# # Refer https://www.alibabacloud.com/help/zh/doc-detail/31837.htm for OSS Region & Endpoint
# OSS_ENDPOINT = 'oss-cn-beijing.aliyuncs.com'

DINGTALK_WEB_HOOK = 'https://oapi.dingtalk.com/robot/send?access_token=f51af59c165a1f1ab08f3d9e5f04098c424a346e25f50efd57cbfe97b10b2dcd'

## 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
## 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:
LDAP_AUTH_URL = "ldap://47.103.86.8:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "admin"

INSTALLED_APPS += (
    # 'debug_toolbar' # other apps for production site
)

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        'TIMEOUT': 300,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD":"mysecret",
            "SOCKET_CONNECT_TIMEOUT": 5,  # 连接
            "SOCKET_TIMEOUT": 5,  # 读写
        }
    }
}

# Celery application definition
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD = 10
CELERYD_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_work.log")
CELERYBEAT_LOG_FILE = os.path.join(BASE_DIR, "logs", "celery_beat.log")

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# sentry配置
sentry_sdk.init(
    dsn="http://1a12d66d68df409997c149f3e8554d49@47.103.86.8:9000/7",
    integrations=[DjangoIntegration()],

    # 采样率，生产环境访问量过大时，建议调小（不用没一个url请求都记录性能）
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)
