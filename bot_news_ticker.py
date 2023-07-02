#!/usr/bin/env python3
#coding=utf-8

from cgitb import text
import telebot, requests, base64, os
from tempfile import NamedTemporaryFile
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Users ID's who are allowed to use the bot
approved_ids = [
    ID1,
    ID2,
]

# Bot token from https://t.me/BotFather
Token = ""

bot = telebot.TeleBot(Token, parse_mode="HTML")

# Webhooks URL
url_text = 'https://example.com/wp-json/news-ticker/v1/add'
url_media = 'https://example.com/wp-json/wp/v2/media'

# Functions
def header( user, password ):
    credentials = user + ':' + password
    token = base64.b64encode( credentials.encode() )
    header_json = {'Authorization': 'Basic ' + token.decode( 'utf-8' ),
                   'Content-Disposition' : 'attachment; filename=%s'% "test1.jpg"}
    return header_json

def upload_image_to_wordpress( file_path, header_json ):
    media = { 'file': file_path }
    responce = requests.post( url_media, headers = header_json, files = media )
    responce_json = responce.json()
    file_id = responce_json["id"]
    if not file_id:
        return None
    else:
        return file_id

def post_requests( title, media_id = 0, video = False ):

    # "token" is for verification in the REST API
    myobj = { 'token': '', 'title': title, 'media_id': media_id }

    # check if this media_id is video file
    if not video:
        myobj['video'] = "false"
    elif video:
        myobj['video'] = "true"
    
    result = requests.post( url_text, json = myobj )
    return result

# Bot Functions
def first_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard = True)
    markup.add( KeyboardButton("Create news-ticker") )
    return markup

def web_keyboard():
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard = True)
    markup.add( KeyboardButton("news-ticker | text"), KeyboardButton("news-ticker | image"), KeyboardButton("news-ticker | video") )
    return markup

def exit_keyboard():
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard = True)
    markup.add( KeyboardButton("Cancel ❌") )
    return markup

all_keyboards = ["Create news-ticker", "news-ticker | text", "news-ticker | image", "news-ticker | video", "Cancel ❌"]
headers = header( "wordpress_username", "wordpress_application_password" )

@bot.message_handler(commands=['start'])
def startmsg(message):

    if message.from_user.id in approved_ids:
        bot.send_message(message.chat.id, f"""Hi {message.from_user.first_name} Welcome to the news-ticker bot""",reply_markup=first_keyboard())


@bot.message_handler(content_types=['text'])
def input_news_flash_text(message):
    if message.from_user.id in approved_ids:
        global author_name

        if message.text == "Create news-ticker":
            bot.send_message(message.chat.id, "Please select a news-ticker type",reply_markup=web_keyboard())
        elif message.text == "news-ticker | text":
            sent_msg = bot.send_message(message.chat.id, "Please enter text to send",reply_markup=exit_keyboard())
            bot.register_next_step_handler(sent_msg, web_text_handler)
        elif message.text == "news-ticker | image":
            sent_msg = bot.send_message(message.chat.id, "Please send a image and type the flash content in the image caption",reply_markup=exit_keyboard())
            bot.register_next_step_handler(sent_msg, web_image_handler)
        elif message.text == "news-ticker | video":
            sent_msg = bot.send_message(message.chat.id, "Please send a video and type the flash content in the video caption",reply_markup=exit_keyboard())
            bot.register_next_step_handler(sent_msg, web_video_handler)
        elif message.text == "Cancel ❌":
            bot.send_message(message.chat.id, "The operation was cancelled",reply_markup=first_keyboard())

# handel text message
def web_text_handler(message):
    if message.from_user.id in approved_ids:
        if message.text == "Cancel ❌":
            bot.send_message(message.chat.id, "The operation was cancelled",reply_markup=first_keyboard())

        if message.text not in all_keyboards:
            title = message.text
            result = post_requests( title, 0, False )
            if result.status_code == requests.codes.ok:
                bot.send_message(message.chat.id, f"the transaction completed successfully!",reply_markup=first_keyboard())

# handel image message
def web_image_handler(message):
    if message.from_user.id in approved_ids:
        if message.text == "Cancel ❌":
            bot.send_message(message.chat.id, "The operation was cancelled",reply_markup=first_keyboard())

        title = message.caption
        if title is not None and title not in all_keyboards:
            file_path = bot.get_file(message.photo[-1].file_id).file_path
            file = bot.download_file(file_path)

            with NamedTemporaryFile( delete=False,mode="wb",suffix=".jpg" ) as file_tmp :
                file_tmp.write( file )
                file_tmp.flush()
                os.fsync(file_tmp.fileno())

            file_to_send = open( file_tmp.name, "rb" )
            file_id = upload_image_to_wordpress( file_to_send, headers )

            if file_id is not None:
                title = message.caption

                result = post_requests( title, file_id, False )
                if result.status_code == requests.codes.ok:
                    bot.send_message(message.chat.id, f"the transaction completed successfully!",reply_markup=first_keyboard())

# handel video message
def web_video_handler(message):
    if message.from_user.id in approved_ids:
        if message.text == "Cancel ❌":
            bot.send_message(message.chat.id, "The operation was cancelled",reply_markup=first_keyboard())
            
        title = message.caption
        if title is not None and title not in all_keyboards:
            file_path = bot.get_file(message.video.file_id).file_path
            file = bot.download_file(file_path)

            with NamedTemporaryFile( delete=False,mode="wb",suffix=".mp4" ) as file_tmp :
                file_tmp.write( file )

            file_to_send  =  open( file_tmp.name, "rb" )
            file_id = upload_image_to_wordpress( file_to_send, headers )

            if file_id is not None:
                result = post_requests( title, file_id, True )
                if result.status_code == requests.codes.ok:
                    bot.send_message(message.chat.id, f"the transaction completed successfully!",reply_markup=first_keyboard())

bot.infinity_polling()
