from typing import final
from django.conf import settings
from linebotApp.models import *
from linebot import LineBotApi
from linebot.models import DatetimePickerTemplateAction, LocationSendMessage, MessageAction, QuickReplyButton, QuickReply, StickerSendMessage, TextSendMessage, TemplateSendMessage, ConfirmTemplate, MessageTemplateAction, ButtonsTemplate, PostbackTemplateAction, URITemplateAction, CarouselTemplate, CarouselColumn, ImageCarouselTemplate, ImageCarouselColumn, ImageSendMessage
import datetime
import requests
from urllib.request import urlretrieve
from django.db import connection


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
    job_type = flist[6]
    job_title = flist[7]
    job_title2 = flist[8]
    lineid = lineId
    if(job_title == 'true'):
        job_title = '是'
    else:
        job_title = '否'
    if(job_title2 == 'true'):
        job_title2 = '是'
    else:
        job_title2 = '否'

    user = job_hunting.objects.create(
        name=name, minSalary=minSalary,
        maxSalary=maxSalary, address=address,
        Phone=Phone, lineId=lineId, remark=remark, job_type=job_type,
        job_title=job_title, job_title2=job_title2)
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
    job_type = flist[9]
    welfare = flist[10]

    user = company.objects.create(
        companyName=companyName, name=name, minSalary=minSalary, maxSalary=maxSalary, address=address, Phone=Phone,
        remark=remark, assistant=assistant, overtime_pay=overtime_pay, lineId=lineId, job_type = job_type, welfare = welfare)
    user.save()
    
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='註冊成功！' + '\n' + '現在可以開始使用求才功能'))


def select_job(event, msg):
    flist = msg[5:].split('&')
    Smin = flist[0]
    Smax = flist[1]
    address = flist[2]
    assistant = flist[3]
    overtime_pay = flist[4]
    job_type = flist[5]
    
    # cursor = connection.cursor()
    # sql = job_type[2:]
    # cursor.execute(sql)
    if(assistant == 'true'):
        assistant = '是'
    else:
        assistant = '否'
    if(overtime_pay == 'true'):
        overtime_pay = '是'
    else:
        overtime_pay = '否'
    if address[3:] == '不拘':
        address = address[:3] + '%'
        if(job_type == '不拘'):
            result = company.objects.raw(
                "select * from linebotApp_company where minSalary >= %s and maxSalary<=%s and address like %s \
                    and assistant=%s and overtime_pay=%s", [Smin, Smax, address, assistant, overtime_pay])
        else:
            result = company.objects.raw(
                "select * from linebotApp_company where job_type=%s and minSalary >= %s and maxSalary<=%s and address like %s \
                    and assistant=%s and overtime_pay=%s", [job_type, Smin, Smax, address, assistant, overtime_pay])
    else:
        if(job_type == '不拘'):
            result = company.objects.raw(
                "select * from linebotApp_company where minSalary >= %s and maxSalary<=%s and address=%s \
                    and assistant=%s and overtime_pay=%s", [Smin, Smax, address, assistant, overtime_pay])
        else:
            result = company.objects.raw(
                "select * from linebotApp_company where job_type=%s and minSalary >= %s and maxSalary<=%s and address=%s \
                    and assistant=%s and overtime_pay=%s", [job_type,Smin, Smax, address, assistant, overtime_pay])
    print(result)
    message = ''
    count = 0
    if(len(result) == 0):
        message = '查無資料！'
    else:
        for i in result:
            count += 1
            if(count != len(result)):
                message += '執業場所名稱：' + str(i.companyName) + '\n' \
                    '聯絡人：' + str(i.name) + '\n'\
                    '工作性質：' + str(i.job_type) + '\n'\
                    '提供薪資：' + str(i.minSalary)+'~' + str(i.maxSalary) + '\n'\
                    '聯絡電話：' + str(i.Phone) + '\n'\
                    '工作地點：' + str(i.address) + '\n'\
                    '備註：' + str(i.remark) + '\n'\
                    '是否有提供助理：' + str(i.assistant) + '\n'\
                    '是否有提供加班費：' + str(i.overtime_pay) + '\n'\
                    '福利：' + str(i.welfare) + '\n\n'
            else:
                message += '執業場所名稱：' + str(i.companyName) + '\n' \
                    '聯絡人：' + str(i.name) + '\n'\
                    '工作性質：' + str(i.job_type) + '\n'\
                    '提供薪資：' + str(i.minSalary)+'~' + str(i.maxSalary) + '\n'\
                    '聯絡電話：' + str(i.Phone) + '\n'\
                    '工作地點：' + str(i.address) + '\n'\
                    '備註：' + str(i.remark) + '\n'\
                    '是否有提供助理：' + str(i.assistant) + '\n'\
                    '是否有提供加班費：' + str(i.overtime_pay) + '\n'\
                    '福利：' + str(i.welfare)

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(message))


def select_staff(event, msg):
    flist = msg[5:].split('&')
    Smin = flist[0]
    Smax = flist[1]
    address = flist[2]
    if address[3:] == '不拘':
        address = address[:3] + '%'
        result = job_hunting.objects.raw(
            "select * from linebotApp_job_hunting where minSalary >= %s and maxSalary<=%s and address like %s", [Smin, Smax, address])
    else:
        result = job_hunting.objects.raw(
            "select * from linebotApp_job_hunting where minSalary >= %s and maxSalary<=%s and address=%s", [Smin, Smax, address])
    message = ''
    count = 0
    if(len(result) == 0):
        message = '查無資料！'
    else:
        for i in result:
            count += 1
            if(count != len(result)):
                message += '姓名：' + str(i.name) + '\n'\
                    '期望薪資：' + str(i.minSalary)+'~' + str(i.maxSalary) + '\n'\
                    '聯絡電話：' + str(i.Phone) + '\n'\
                    '期望工作地點：' + str(i.address) + '\n'\
                    '備註：' + str(i.remark) + '\n\n'
            else:
                message += '姓名：' + str(i.name) + '\n'\
                    '提供薪資：' + str(i.minSalary)+'~' + str(i.maxSalary) + '\n'\
                    '聯絡電話：' + str(i.Phone) + '\n'\
                    '工作地點：' + str(i.address) + '\n'\
                    '備註：' + str(i.remark)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(message))
