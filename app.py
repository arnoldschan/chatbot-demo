from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import InvalidSignatureError
from linebot.models import TextSendMessage
import json
import requests
from dynamodb import DynamoDB


access_token = <<YOUR ACCESS TOKEN HERE>>
channel_secret= <<YOUR CHANNEL SECRET HERE>>
table_name = 'echobot'
key_name = 'userID'
sec_key_name = 'timestamp'

def lambda_handler(event,context):
    line_bot = BotEcho(
        event,
        access_token = access_token ,
        channel_secret = channel_secret)

    if line_bot.signature_check != 200:
        print("fail to signature check")
        return {'statusCode': line_bot.signature_check}

    response = line_bot.send_reply(line_bot.text_message)

    if response != 200:
        print('fail to send reply')
        return {'statusCode': response}

    return {'statusCode':200}

class BotEcho:
    def __init__(self,event,access_token,channel_secret):
        self.event = event
        self.bot = LineBotApi(access_token)
        self.handler = WebhookHandler(channel_secret)
        self.body = json.loads(event['body'])['events'][0]
        self.sender_id = self.body['source']['userId']
        self.text_message = self.body['message']['text']
        self.log(sender=self.sender_id,to='self',message=self.text_message)
    @property
    def signature_check(self):
        signature = self.event['headers']['X-Line-Signature']
        try:
            self.handler.handle(self.event['body'], signature)
            return 200
        except InvalidSignatureError:
            return 400

    def send_reply(self,message):
        self.log(sender='self',to=self.sender_id,message=message)
        response = self.bot.reply_message(self.body['replyToken'], \
                                    TextSendMessage(text=message))
        return response

    def log(self,sender,to,message):
        log_head = ['to','message']
        log_value = [to, message]
        response = DynamoDB(table_name, key_name, sec_key_name)\
                                .put(sender,log_head,log_value)
        print(response)
        return response