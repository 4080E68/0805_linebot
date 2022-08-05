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
            if msg[:7] == '@登記求職資料' and len(msg) > 3:
                func.job_register(event, msg, lineId)
            if msg[:7] == '@確認修改資料' and len(msg) > 3:
                func.update_job(event, msg, lineId)
            if msg == '@求職資料修改':
                if job_hunting.objects.filter(lineId=lineId).exists():
                    url = 'https://joblinebotapp.herokuapp.com/' + str(lineId)
                    line_bot_api.reply_message(
                        event.reply_token, TextSendMessage(text=url))
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

    return render(request, 'update_job.html', locals())
