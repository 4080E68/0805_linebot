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
            if msg == '@我要求職':
                func.job(event, lineId)
            if msg == '@查詢登記資料':
                if job_hunting.objects.filter(lineId=lineId).exists():
                    data = job_hunting.objects.get(lineId=lineId)
                    message = '姓名：' + str(data.name) + '\n' + '期望薪資：' + '時薪' + str(data.minSalary) + '~' + str(data.maxSalary) + \
                        '\n' + '聯絡電話：' + str(data.Phone) + \
                        '\n'+'期望工作地點：' + str(data.address) + \
                        '\n'+'備註：' + str(data.remark)
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=message))
                else:
                    errorMessage = ''
                    errorMessage += '查無資料' + '\n' + '請先至求職資料設定登記求職資料'
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=errorMessage))
            if msg[:7] == '@登記求職資料' and len(msg) > 3:
                func.job_register(event, msg, lineId)
            if msg[:7] == '@登記求才資料' and len(msg) > 3:
                func.company_register(event, msg, lineId)
            # if msg[:7] == '@確認修改資料' and len(msg) > 3:
            #     func.update_job(event, msg, lineId)
            if msg == '@求職資料設定':
                if job_hunting.objects.filter(lineId=lineId).exists():
                    url = 'https://joblinebotapp.herokuapp.com/updateDate/' + \
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
                    url = 'https://joblinebotapp.herokuapp.com/updateDate/' + \
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


def update_job(request, id):
    if job_hunting.objects.filter(lineId=id).exists():
        userData = job_hunting.objects.get(lineId=id)
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

        if job_hunting.objects.filter(lineId=id).exists():
            try:
                job_hunting.objects.filter(lineId=id).update(
                    name=name, minSalary=minSalary, maxSalary=maxSalary, address=address, Phone=phone, remark=remark
                )
            except:
                message = '修改失敗！'
    return render(request, 'update_job.html', locals())
