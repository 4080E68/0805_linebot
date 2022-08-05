from django.conf import settings
from linebotApp.models import *
from linebot import LineBotApi
from linebot.models import DatetimePickerTemplateAction, LocationSendMessage, MessageAction, QuickReplyButton, QuickReply, StickerSendMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImageSendMessage
import datetime
import requests
from urllib.request import urlretrieve

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)


def job(event, lineId):  # 求職函式
    if job_hunting.objects.filter(lineId=lineId).exists():
        userData = job_hunting.objects.get(lineId=lineId)
        userName = userData.name
        message = str(userName) + '您好今天想找什麼樣的工作呢？'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=message))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='查無資料'))


def job_register(event, msg, lineId):  # 註冊資料
    flist = msg[7:].split('&')
    name = flist[0]
    salary = flist[1]
    address = flist[2]
    Phone = flist[3]
    lineid = lineId
    print(name, salary, address, Phone, lineid)
    if job_hunting.objects.filter(lineId=lineId).exists():
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='此line帳號已有資料，請勿重複登記！'))
    else:
        user = job_hunting.objects.create(
            name=name, salary=salary, address=address, Phone=Phone, lineId=lineid)
        user.save()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='註冊成功！'))


def update_job(event, msg, lineId):  # 修改資料
    flist = msg[7:].split('&')
    name = flist[0]
    salary = flist[1]
    address = flist[2]
    Phone = flist[3]
    lineid = lineId

    print(name, salary, address, Phone, lineid)
    if job_hunting.objects.filter(lineId=lineId).exists():
        try:
            job_hunting.objects.filter(lineId=lineId).update(
                name=name, salary=salary, address=address, Phone=Phone, lineId=lineid
            )
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='修改成功！'))
        except:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text='修改失敗！'))
    else:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='查無資料請確認是否有進行註冊！'))
