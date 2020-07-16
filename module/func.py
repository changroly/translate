from django.conf import settings

from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, AudioSendMessage
from linebot.models import TemplateSendMessage,\
    ButtonsTemplate, URITemplateAction, MessageTemplateAction, CarouselTemplate, CarouselColumn
import variable_settings as varset
from translate import Translator
from urllib.parse import quote

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)

import datetime
import pymongo
from pymongo import MongoClient
import urllib.parse
Authdb='bot'

def sendQnA(event, mtext):
    client = MongoClient('mongodb://roly:dayi3774@cluster0-shard-00-00.0mtts.mongodb.net:27017,cluster0-shard-00-01.0mtts.mongodb.net:27017,cluster0-shard-00-02.0mtts.mongodb.net:27017/<dbname>?ssl=true&replicaSet=atlas-da52w8-shard-0&authSource=admin&retryWrites=true&w=majority')
    db = client[Authdb]
    collect = db['translator']
    collect.insert({"id": event.source.user_id,
                    "date": datetime.datetime.utcnow(),
                    "buy": 'no',
                    "text": mtext
                    })

def send(event):  #按鈕樣版
    try:
        message = TemplateSendMessage(
            alt_text='24HBOT',
            template=ButtonsTemplate(
                thumbnail_image_url='https://i.imgur.com/ts7gkps.png',  #顯示的圖片
                title='LINE對話機器人將會是下一個世代的App',  #主標題
                text='LINE在台灣擁有2100萬用戶,對台灣的公司商家而言，有90%的使用者不需要額外下載新的App，就可以溝通互動。',  #副標題
                actions=[
                    URITemplateAction(  #開啟網頁
                        label='更多各行各業對話機器人',
                        uri='https://www.chatbizz.biz'
                    ),                    
                    URITemplateAction(  #開啟網頁
                        label='更多免費LINE APP',
                        uri='https://lin.ee/2EcRPEUs9'
                    ),
                    URITemplateAction(
                        label='訂閱或訂購',
                        uri='https://unitbesto.wixsite.com/mysite'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))     



def showUse(event):
    try:
        text1 = '''1. 直接輸入中文，可翻譯為多國語言。
2. 直接輸入外文(輸入的外文前須加"#")，可翻譯回中文。'''
                
        message = TextSendMessage(
            text = text1
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def setLang(event, lang, sound, userid):  #設定翻譯語言
    try:
        varset.set(userid, lang + '/' + sound)
        message = TextSendMessage(
            text = '語言：' + langtoword(lang)
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))

def setElselang(event):  #設定其他語言
    try:
        message = TextSendMessage(
            text = '選擇語言：',
            quick_reply = QuickReply(  #使用快速選單
                items = [
                    QuickReplyButton(
                        action = PostbackAction(label='英文en', data='item=en')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='日文ja', data='item=ja')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='韓文ko', data='item=ko')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='泰文th', data='item=th')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='越南文vi', data='item=vi')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='印尼文id', data='item=id')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='法文fr', data='item=fr')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='德文de', data='item=de')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='西班牙文es', data='item=es')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='荷蘭文nl', data='item=nl')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='義大利文it', data='item=it')
                    ),
                    QuickReplyButton(
                        action = PostbackAction(label='緬文my', data='item=my')
                    ),
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))




def sendTranslate(event, lang, sound, mtext):  #翻譯及朗讀
    try:
        translator = Translator(from_lang="zh-Hant", to_lang=lang)  #來源是中文,翻譯後語言為lang
        translation = translator.translate(mtext)  #進行翻譯
        if sound == 'yes':  #發音
            text = quote(translation)
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query=' + text + '&language=' + lang  #使用google語音API
            message = [  #若要發音需傳送文字及語音,必須使用陣列
                TextSendMessage(  #傳送翻譯後文字
                    text = translation
                ),
                AudioSendMessage(  #傳送語音
                    original_content_url = stream_url,
                    duration=20000  
                ),
            ]
        else:  #不發音
            message = TextSendMessage(
                text = translation
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendTranslate2(event, lang, sound, mtext):  #翻譯及朗讀
    try:
        translator = Translator(from_lang=lang, to_lang="zh-Hant")  #來源是中文,翻譯後語言為lang
        translation = translator.translate(mtext[1:])  #進行翻譯
        if sound == 'yes':  #發音
            text = quote(translation)
            stream_url = 'https://google-translate-proxy.herokuapp.com/api/tts?query=' + text + '&language=' + "zh-Hant"  #使用google語音API
            message = [  #若要發音需傳送文字及語音,必須使用陣列
                TextSendMessage(  #傳送翻譯後文字
                    text = translation
                ),
                AudioSendMessage(  #傳送語音
                    original_content_url = stream_url,
                    duration=20000  
                ),
            ]
        else:  #不發音
            message = TextSendMessage(
                text = translation
            )
        line_bot_api.reply_message(event.reply_token,message)
    except:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text='發生錯誤！'))
def sendData(event, backdata, sound, userid):  #設定其他語言
    lang = backdata.get('item')  #取得快速選單的選取值
    setLang(event, lang, sound, userid)  #設定翻譯語言

def langtoword(lang):  #將語言代碼轉為中文字
    if lang == 'en':  word = '英文en'
    elif lang == 'ja':  word = '日文ja'
    elif lang == 'ko':  word = '韓文ko'
    elif lang == 'th':  word = '泰文th'
    elif lang == 'vi':  word = '越南文vi'
    elif lang == 'id':  word = '印尼文id'
    elif lang == 'fr':  word = '法文fr'
    elif lang == 'de':  word = '德文de'
    elif lang == 'es':  word = '西班牙文es'
    elif lang == 'nl':  word = '荷蘭文nl'
    elif lang == 'it':  word = '義大利文it'
    elif lang == 'my':  word = '緬文my'

    return word

