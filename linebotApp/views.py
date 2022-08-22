from ast import Delete
from cmath import log
from django.shortcuts import render
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from linebotApp import func
from linebotApp.models import *

# Create your views here.
line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        # 先設定一個要回傳的message空集合

        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)

        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                msg = event.message.text
                lineId = events[0].source.user_id
            if msg[:5] == '@搜尋求職' and len(msg) > 3:
                func.select_job(event, msg)
            if msg[:5] == '@搜尋求才' and len(msg) > 3:
                func.select_staff(event, msg)
            if msg == '@查詢登記資料':
                if job_hunting.objects.filter(lineId=lineId).exists():
                    data = job_hunting.objects.filter(lineId=lineId)
                    message = ''
                    count = 0
                    for i in data:
                        count += 1
                        if(count < len(data)):
                            if(i.job_type == '全職'):
                                if(i.job_title == 'true'):
                                    i.job_title = '是'
                                else:
                                    i.job_title = '否'
                                if(i.job_title2 == 'true'):
                                    i.job_title2 = '是'
                                else:
                                    i.job_title2 = '否'
                                message += '姓名：' + str(i.name) + \
                                    '\n'+'工作種類：' + str(i.job_type) + \
                                    '\n' + '期望薪資：' + '月薪' + str(i.minSalary) + '~' + str(i.maxSalary) + \
                                    '\n' + '聯絡電話：' + str(i.Phone) + \
                                    '\n'+'期望工作地點：' + str(i.address) + \
                                    '\n'+'備註：' + str(i.remark) + \
                                    '\n'+'擔任負責人：' + str(i.job_title) + \
                                    '\n'+'擔任非負責人：' + str(i.job_title2) + '\n\n'
                            else:
                                message += '姓名：' + str(i.name) + \
                                    '\n'+'工作種類：' + str(i.job_type) + \
                                    '\n' + '期望薪資：' + '時薪' + str(i.minSalary) + '~' + str(i.maxSalary) + \
                                    '\n' + '聯絡電話：' + str(i.Phone) + \
                                    '\n'+'期望工作地點：' + str(i.address) + \
                                    '\n'+'備註：' + str(i.remark) + '\n\n'
                        else:
                            if(i.job_type == '全職'):
                                if(i.job_title == 'true'):
                                    i.job_title = '是'
                                else:
                                    i.job_title = '否'
                                if(i.job_title2 == 'true'):
                                    i.job_title2 = '是'
                                else:
                                    i.job_title2 = '否'
                                message += '姓名：' + str(i.name) + \
                                    '\n'+'工作種類：' + str(i.job_type) + \
                                    '\n' + '期望薪資：' + '月薪' + str(i.minSalary) + '~' + str(i.maxSalary) + \
                                    '\n' + '聯絡電話：' + str(i.Phone) + \
                                    '\n'+'期望工作地點：' + str(i.address) + \
                                    '\n'+'備註：' + str(i.remark) + \
                                    '\n'+'擔任負責人：' + str(i.job_title) + \
                                    '\n'+'擔任非負責人：' + str(i.job_title2)
                            else:
                                message += '姓名：' + str(i.name) + \
                                    '\n'+'工作種類：' + str(i.job_type) + \
                                    '\n' + '期望薪資：' + '時薪' + str(i.minSalary) + '~' + str(i.maxSalary) + \
                                    '\n' + '聯絡電話：' + str(i.Phone) + \
                                    '\n'+'期望工作地點：' + str(i.address) + \
                                    '\n'+'備註：' + str(i.remark)
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=message))
                else:
                    errorMessage = ''
                    errorMessage += '查無資料' + '\n' + '請先至求職資料設定登記求職資料'
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=errorMessage))

            if msg == '@求才資料設定':
                if company.objects.filter(lineId=lineId).exists():
                    url = 'https://w1.linebot.com.tw/selectCompany/%s' % lineId
                    line_bot_api.reply_message(
                        event.reply_token, FlexSendMessage(
                            alt_text='搜尋結果',
                            contents={
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "登記求才資料",
                                            "size": "lg",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md",
                                            "color": "#000000"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "uri",
                                                "label": "前往登記",
                                                "uri": 'https://liff.line.me/1656626380-YA6qXpd1'
                                            },
                                            "style": "primary",
                                            "margin": "md"
                                        },
                                        {
                                            "type": "text",
                                            "text": "查看求才資料",
                                            "size": "lg",
                                            "margin": "md",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md",
                                            "color": "#000000"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "uri",
                                                "label": "前往查看",
                                                "uri": url
                                            },
                                            "style": "secondary",
                                            "margin": "md"
                                        },
                                    ]
                                }
                            }
                        )
                    )
                else:
                    errorMessage = ''
                    errorMessage += '查無資料' + '\n' + '請先至求才資料設定登記求職資料'
                    message = []

                    message.append(TextSendMessage(text=errorMessage))
                    message.append(FlexSendMessage(
                        alt_text='搜尋結果',
                        contents={
                            "type": "bubble",
                            "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "登記求才資料",
                                            "size": "lg",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md",
                                            "color": "#000000"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "uri",
                                                "label": "前往登記",
                                                "uri": 'https://liff.line.me/1656626380-YA6qXpd1'
                                            },
                                            "style": "primary",
                                            "margin": "md"
                                        },
                                    ]
                            }
                        }
                    )
                    )
                    line_bot_api.reply_message(
                        event.reply_token, message)
            if msg[:7] == '@登記求職資料' and len(msg) > 3:
                func.job_register(event, msg, lineId)
            if msg[:7] == '@登記求才資料' and len(msg) > 3:
                func.company_register(event, msg, lineId)
            if msg == '@求職資料設定':
                if job_hunting.objects.filter(lineId=lineId).exists():
                    url = 'https://w1.linebot.com.tw/update_job/' + \
                        str(lineId)
                    line_bot_api.reply_message(
                        event.reply_token, FlexSendMessage(
                            alt_text='搜尋結果',
                            contents={
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "求職資料登記",
                                                    "size": "lg",
                                                    "weight": "bold"
                                                },
                                                {
                                                    "type": "separator",
                                                    "margin": "md",
                                                    "color": "#000000"
                                                },
                                                {
                                                    "type": "button",
                                                    "action": {
                                                        "type": "uri",
                                                        "label": "求職資料登記",
                                                        "uri": "https://liff.line.me/1656626380-ZrL4j5xO"
                                                    },
                                                    "style": "secondary",
                                                    "margin": "md"
                                                },
                                                {
                                                    "type": "text",
                                                    "text": "查詢登記資料",
                                                    "size": "lg",
                                                    "weight": "bold"
                                                },
                                                {
                                                    "type": "separator",
                                                    "margin": "md",
                                                    "color": "#000000"
                                                },
                                                {
                                                    "type": "button",
                                                    "action": {
                                                        "type": "message",
                                                        "label": "查詢登記資料",
                                                        "text": "@查詢登記資料"
                                                    },
                                                    "style": "secondary",
                                                    "margin": "md"
                                                }
                                            ],
                                            "margin": "lg"
                                        },
                                        {
                                            "type": "box",
                                            "layout": "vertical",
                                            "contents": [
                                                {
                                                    "type": "text",
                                                    "text": "求職資料修改",
                                                    "size": "lg",
                                                    "weight": "bold"
                                                },
                                                {
                                                    "type": "separator",
                                                    "margin": "md",
                                                    "color": "#000000"
                                                },
                                                {
                                                    "type": "button",
                                                    "action": {
                                                        "type": "uri",
                                                        "label": "前往修改",
                                                        "uri": url
                                                    },
                                                    "style": "secondary",
                                                    "margin": "md"
                                                }
                                            ],
                                            "margin": "lg"
                                        }
                                    ]
                                }
                            }))
                else:
                    line_bot_api.reply_message(
                        event.reply_token, FlexSendMessage(
                            alt_text='搜尋結果',
                            contents={
                                "type": "bubble",
                                "body": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "求職資料登記",
                                            "size": "lg",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "separator",
                                            "margin": "md",
                                            "color": "#000000"
                                        },
                                        {
                                            "type": "button",
                                            "action": {
                                                "type": "uri",
                                                "label": "求職資料登記",
                                                "uri": "https://liff.line.me/1656626380-ZrL4j5xO"
                                            },
                                            "style": "secondary",
                                            "margin": "md"
                                        },
                                    ]
                                }
                            }
                        )
                    )

            if msg == '@求職資料修改':
                if job_hunting.objects.filter(lineId=lineId).exists():
                    url = 'https://w1.linebot.com.tw/update_job/' + \
                        str(lineId)
                    line_bot_api.reply_message(
                        event.reply_token, FlexSendMessage(
                            alt_text='搜尋結果',
                            contents={
                                "type": "bubble",
                                "footer": {
                                    "type": "box",
                                    "layout": "vertical",
                                    "spacing": "sm",
                                    "contents": [
                                        {
                                            "type": "text",
                                            "text": "修改連結",
                                            "margin": "sm",
                                            "size": "xl",
                                            "weight": "bold"
                                        },
                                        {
                                            "type": "separator"
                                        },
                                        {
                                            "type": "button",
                                            "style": "primary",
                                            "height": "sm",
                                            "action": {
                                                "type": "uri",
                                                "label": "前往修改",
                                                "uri": url
                                            },
                                            "margin": "lg"
                                        }
                                    ],
                                    "flex": 0
                                }
                            }))
                else:
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text='查無資料請確認是否有進行註冊！'))

        return HttpResponse()

    else:
        return HttpResponseBadRequest()


@csrf_exempt
def update_job(request, lineId, id):
    if job_hunting.objects.filter(lineId=lineId).exists() and job_hunting.objects.filter(id=id).exists():
        userData = job_hunting.objects.get(id=id)
        data = job_hunting.objects.get(id=id)
        userName = userData.name
        userminSalary = userData.minSalary
        usermaxSalary = userData.maxSalary
        userCounty = userData.address[:3]
        userAddress = userData.address[3:]
        userPhone = userData.Phone
        userRemark = userData.remark
    if request.method == "POST":
        name = request.POST['name']
        minSalary = request.POST['minSalary']
        maxSalary = request.POST['maxSalary']
        address = request.POST['County']+request.POST['address']
        phone = request.POST['phone']
        remark = request.POST['remark']
        job_type = request.POST['job_type']
        job_title = request.POST.get('job_title')
        job_title2 = request.POST.get('job_title2')
        if(job_title != None):
            job_title = '是'
        else:
            job_title = '否'
        if(job_title2 != None):
            job_title2 = '是'
        else:
            job_title2 = '否'
        print(name, minSalary, maxSalary, address, phone,
              remark, job_type, job_title, job_title2)

        if job_hunting.objects.filter(id=id).exists():
            try:
                job_hunting.objects.filter(id=id).update(
                    name=name, minSalary=minSalary, maxSalary=maxSalary, address=address, Phone=phone, remark=remark, job_type=job_type, job_title=job_title, job_title2=job_title2
                )
            except:
                message = '修改失敗！'
        data = job_hunting.objects.get(id=id)
        userName = userData.name
        userminSalary = userData.minSalary
        usermaxSalary = userData.maxSalary
        userCounty = userData.address[:3]
        userAddress = userData.address[3:]
        userPhone = userData.Phone
        userRemark = userData.remark
    return render(request, 'update_job.html', locals())


@csrf_exempt
def select_job(request, id):
    if job_hunting.objects.filter(lineId=id).exists():
        data = job_hunting.objects.filter(lineId=id)  # 搜尋所有資料
    if request.method == "POST":
        id = request.POST['del']
        if(id == 'NO'):
            pass
        else:
            if job_hunting.objects.filter(id=id).exists():
                delData = job_hunting.objects.get(id=id)
                delData.delete()
    return render(request, 'select_job.html', locals())


@csrf_exempt
def selectCompany(request, id):
    if company.objects.filter(lineId=id).exists():
        data = company.objects.filter(lineId=id)  # 搜尋所有資料
    if request.method == "POST":
        id = request.POST['del']
        if(id == 'NO'):
            pass
        else:
            if company.objects.filter(id=id).exists():
                delData = company.objects.get(id=id)
                delData.delete()
    return render(request, 'selectCompany.html', locals())


@csrf_exempt
def update_Company(request, lineId, id):
    if company.objects.filter(id=id).exists() and company.objects.filter(lineId=lineId).exists():
        data = company.objects.get(id=id)  # 搜尋所有資料
        dataCounty = data.address[:3]
        dataAddress = data.address[3:]
    if request.method == "POST":
        companyName = request.POST['companyName']
        name = request.POST['name']
        minSalary = request.POST['Smin']
        maxSalary = request.POST['Smax']
        address = request.POST['County']+request.POST['address']
        phone = request.POST['phone']
        remark = request.POST['remark']
        assistant = request.POST.get('assistant')
        overtime_pay = request.POST.get('overtime_pay')
        if assistant == 'on':
            assistant = '是'
        else:
            assistant = '否'
        if overtime_pay == 'on':
            overtime_pay = '是'
        else:
            overtime_pay = '否'
        print(companyName, name, minSalary, maxSalary,
              address, phone, remark, assistant, overtime_pay)
        if company.objects.filter(id=id).exists():
            try:
                company.objects.filter(id=id).update(
                    companyName=companyName, name=name,
                    minSalary=minSalary, maxSalary=maxSalary,
                    address=address, Phone=phone, remark=remark,
                    assistant=assistant, overtime_pay=overtime_pay
                )
                data = company.objects.get(id=id)  # 搜尋所有資料
                dataCounty = data.address[:3]
                dataAddress = data.address[3:]
            except:
                print('修改失敗!')
    return render(request, 'updateCompany.html', locals())
