from dingtalkchatbot.chatbot import DingtalkChatbot

from django.conf import settings


# shell测试函数——python manage.py shell --settings=settings.local
def send(message, at_mobiles=[]):
    '''
    钉钉消息通知，需要钉钉群聊设置智能机器人
    :param message:
    :param at_mobiles:
    :return:
    '''
    # 引用settings里面的配置的钉钉群消息通知的WebHook地址
    webhook = settings.DINGTALK_WEB_HOOK

    # 初始化机器人小丁， #方式一：通常初始化方式
    xiaoding = DingtalkChatbot(webhook)

    # 方式二：勾选‘加签’选项时使用（v1.5以上新功能)
    # xiaoding = DingtalkChatbot(webhook,secret=secret)

    # Text消息@所有人
    xiaoding.send_text(msg=('面试通知：%s' % message), at_mobiles=at_mobiles)
