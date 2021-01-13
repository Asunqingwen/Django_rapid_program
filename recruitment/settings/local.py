from .base import *

DEBUG = True

ALLOWED_HOSTS = []

## 务必修改以下值，确保运行时系统安全:
SECRET_KEY = "w$46bks+b3-7f(13#i%v@jwejrnxc$^^#@#@^t@fofizy1^mo9r8(-939243423300"

DINGTALK_WEB_HOOK = 'https://oapi.dingtalk.com/robot/send?access_token=f51af59c165a1f1ab08f3d9e5f04098c424a346e25f50efd57cbfe97b10b2dcd'

## 如果仅使用数据库中的账号，以下 LDAP 配置可忽略
## 替换这里的配置为正确的域服务器配置，同时可能需要修改 base.py 中的 LDAP 服务器相关配置:
LDAP_AUTH_URL = "ldap://47.103.86.8:389"
LDAP_AUTH_CONNECTION_USERNAME = "admin"
LDAP_AUTH_CONNECTION_PASSWORD = "admin"

INSTALLED_APPS += (
    # 'debug_toolbar' # other apps for production site
)
