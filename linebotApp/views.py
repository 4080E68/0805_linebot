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
                    message = '姓名：' + str(data.name) + '\n' + '期望薪資：' + str(data.salary) + \
                        '\n' + '聯絡電話：' + str(data.Phone) + \
                        '\n'+'期望工作地點：' + str(data.address)
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=message))
            if msg[:7] == '@登記求職資料' and len(msg) > 3:
                func.job_register(event, msg, lineId)
            # if msg[:7] == '@確認修改資料' and len(msg) > 3:
            #     func.update_job(event, msg, lineId)
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
        userSalary = userData.salary[2:]
        userSalary1 = userData.salary
        userAddress = userData.address
        userPhone = userData.Phone
    if request.method == "POST":
        name = request.POST['name']
        select = request.POST['select']
        salary = request.POST['salary']
        finalSalary = select + salary
        address = request.POST['address']
        phone = request.POST['phone']
        if job_hunting.objects.filter(lineId=id).exists():
            try:
                job_hunting.objects.filter(lineId=id).update(
                    name=name, salary=finalSalary, address=address, Phone=phone
                )
            except:
                message = '修改失敗！'
    return render(request, 'update_job.html', locals())
