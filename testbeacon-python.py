import os
import linebot.v3.messaging
from linebot.v3.messaging.models.user_profile_response import UserProfileResponse
from linebot.v3.messaging.rest import ApiException

from linebot.models import (
 MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,
 SourceUser, SourceGroup, SourceRoom,
 TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
 ButtonsTemplate, URITemplateAction, PostbackTemplateAction,
 CarouselTemplate, CarouselColumn, PostbackEvent,
 StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
 ImageMessage, VideoMessage, AudioMessage,
 UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)
from linebot.models.template import *
from linebot import (
    LineBotApi, WebhookHandler
)

from pprint import pprint
from flask import Flask, jsonify, render_template, request
import json
import numpy as np


app = Flask(__name__)
# Defining the host is optional and defaults to https://api.line.me
# See configuration.py for a list of all supported configuration parameters.
configuration = linebot.v3.messaging.Configuration(
    host="https://api.line.me",
    access_token= "rPPYWtGcQfPtzw9ofrZfod1VgeqapWbDgMkXIKu38UgjnPtNHkMm5wbNVcDf/9klZ7PRZ8uJoh03XUSpTES9GxoSo1JL6kzo2p7OBhwEnX+25YJb+4ENLAma3VSNbnm43Uz3rtJRhAdTm3gv6sGnvQdB04t89/1O/w1cDnyilFU="
    
)
accesstoken= "rPPYWtGcQfPtzw9ofrZfod1VgeqapWbDgMkXIKu38UgjnPtNHkMm5wbNVcDf/9klZ7PRZ8uJoh03XUSpTES9GxoSo1JL6kzo2p7OBhwEnX+25YJb+4ENLAma3VSNbnm43Uz3rtJRhAdTm3gv6sGnvQdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(accesstoken) 
####################### new ########################
@app.route('/')
def index():
    return "Hello World! Test OK."


@app.route('/webhook', methods=['POST'])
def callback():
    json_line = request.get_json(force=False,cache=False)
    json_line = json.dumps(json_line)
    decoded = json.loads(json_line)
    no_event = len(decoded['events'])
    for i in range(no_event):
        event = decoded['events'][i]
        event_handle(event)
    return '',200

def event_handle(event):
    print(event)
    print("\n")
    whookevent = event
    
    # Enter a context with an instance of the API client
    with linebot.v3.messaging.ApiClient(configuration) as api_client:
        # Create an instance of the API class
        api_instance = linebot.v3.messaging.MessagingApi(api_client)
        #user_id = 'U1fe4d1b000bf8216ebc2b6b33f15bc56'  # Replace this with the actual User ID you want to get the profile for
        try:
            userId = event['source']['userId']
        except:
            print('error cannot get userId')
            return ''
        try:
            retoken = event['replyToken']
        except:
            print('error cannot get rtoken')
            return ''
        try:
            api_response = api_instance.get_profile(userId)
            print("get_profile:")
            pprint(api_response)
            print("\n")
        except Exception as e:
            print("Exception when calling MessagingApi->get_profile: %s\n" % e)

        if event['type'] == 'beacon':  # ตรวจสอบว่าเหตุการณ์เป็น Beacon Event หรือไม่
            # ดึงข้อมูลเกี่ยวกับ Beacon Event
            hwid = event['beacon']['hwid']  # Hardware ID ของ Beacon
            dm = event['beacon']['dm']      # ข้อมูลส่วนเสริม (optional)
            type = event['beacon']['type']  # ประเภทของ Beacon (enter, leave, banner)

            if type == 'enter':
                reply_msg = 'Beacon Enter'
                print("Beacon Enter")
            elif type == 'leave':
                reply_msg = 'Beacon Leave'
                print("Beacon Leave")
            else:
                reply_msg = 'Beacon Event Unknown'
                print("Beacon Unknown")

            line_bot_api.reply_message(event['replyToken'], TextSendMessage(text=reply_msg))
            line_bot_api.push_message(event['source']['userId'], TextSendMessage(text=f"สถานะข้อความ: {whookevent}"))

        
        elif event['type'] == 'message':
            # ตรวจสอบประเภทของข้อความ หากเป็นสติกเกอร์ (sticker)
            if 'sticker' in event['message']:
                reply_msg = 'Got Sticker'
               
            else:
                message_text = event['message']['text']
                reply_msg = f"{message_text}"
            
            line_bot_api.reply_message(event['replyToken'], TextSendMessage(text=reply_msg))
            #line_bot_api.push_message(event['source']['userId'], TextSendMessage(text=f"สถานะข้อความ: {whookevent}"))

            # ส่งข้อมูลโปรไฟล์กลับไปยังผู้ใช้งาน LINE OA (ตัวอย่าง)
        try:
            display_name = api_response.display_name
            status_message = api_response.status_message
            picture_url = api_response.picture_url
            whookevent = event

        except AttributeError:
            display_name = "ไม่พบข้อมูลชื่อผู้ใช้"

        #line_bot_api.push_message(event['source']['userId'], TextSendMessage(text=f"ชื่อผู้ใช้: {display_name}"))
        #line_bot_api.push_message(event['source']['userId'], TextSendMessage(text=f"รูปโปรไฟล์: {picture_url}"))
        #line_bot_api.push_message(event['source']['userId'], TextSendMessage(text=f"สถานะโปรไฟล์: {status_message}"))
        #line_bot_api.push_message(event['source']['userId'], TextSendMessage(text=f"สถานะข้อความ: {whookevent}"))

        print("\n")

if __name__ == '__main__':
    app.run(debug=True)
