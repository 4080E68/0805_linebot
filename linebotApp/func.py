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
        errorMessage = ''
        errorMessage += '查無資料' + '\n' + '請先至求職資料設定登記求職資料'
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=errorMessage))


def job_register(event, msg, lineId):  # 註冊資料
    flist = msg[7:].split('&')
    name = flist[0]
    minSalary = flist[1]
    maxSalary = flist[2]
    address = flist[3]
    Phone = flist[4]
    remark = flist[5]
    lineid = lineId

    if job_hunting.objects.filter(lineId=lineId).exists():
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='此line帳號已有資料，請勿重複登記！'))
    else:
        user = job_hunting.objects.create(
            name=name, minSalary=minSalary, maxSalary=maxSalary, address=address, Phone=Phone, lineId=lineId, remark=remark)
        user.save()
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='註冊成功！' + '\n' + '現在可以開始使用求職功能'))


def company_register(event, msg, lineId):  # 求才註冊資料
    flist = msg[7:].split('&')
    companyName = flist[0]
    name = flist[1]
    minSalary = flist[2]
    maxSalary = flist[3]
    address = flist[4]
    Phone = flist[5]
    remark = flist[6]
    assistant = flist[7]
    overtime_pay = flist[8]
    print(flist)
    user = company.objects.create(
        companyName=companyName, name=name, minSalary=minSalary, maxSalary=maxSalary, address=address, Phone=Phone,
        remark=remark, assistant=assistant, overtime_pay=overtime_pay, lineId=lineId)
    user.save()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='註冊成功！' + '\n' + '現在可以開始使用求才功能'))

# def update_job(event, msg, lineId):  # 修改資料
#     flist = msg[7:].split('&')
#     name = flist[0]
#     salary = flist[1]
#     address = flist[2]
#     Phone = flist[3]
#     lineid = lineId

#     print(name, salary, address, Phone, lineid)
#     if job_hunting.objects.filter(lineId=lineId).exists():
#         try:
#             job_hunting.objects.filter(lineId=lineId).update(
#                 name=name, salary=salary, address=address, Phone=Phone, lineId=lineid
#             )
#             line_bot_api.reply_message(
#                 event.reply_token, TextSendMessage(text='修改成功！'))
#         except:
#             line_bot_api.reply_message(
#                 event.reply_token, TextSendMessage(text='修改失敗！'))
#     else:
#         line_bot_api.reply_message(
#             event.reply_token, TextSendMessage(text='查無資料請確認是否有進行註冊！'))
