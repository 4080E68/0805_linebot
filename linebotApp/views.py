from django.shortcuts import render
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import *
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

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
            print(events)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                msg = event.message.text
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text=msg))

            # if msg[:3] == '&&&' and len(msg) > 3:
            #     func2.manageForm(event, msg)
            # if msg == '@健保查詢':
            #     line_bot_api.reply_message(
            #         event.reply_token, TextSendMessage(text='https://liff.line.me/1656626380-Z7knz9PR'))

        return HttpResponse()

    else:
        return HttpResponseBadRequest()
