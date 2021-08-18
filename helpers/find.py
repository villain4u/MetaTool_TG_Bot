import telegram
import telebot
import logging
import requests
from telegraph import Telegraph
from helpers.groupcmd import grpcmd

# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS
PIC = Config.PIC
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
SEARCH_AUTH = Config.SEARCH_AUTH
LD_DOMW = Config.LD_DOMW
APP_INTENT = Config.APP_INTENT

try:
    ADMIN_LIST = ADMIN_IDS 
    restricted_mode = True
except:
    ADMIN_LIST = []  # ==> Do Not Touch This !!
    restricted_mode = False

bot = telebot.TeleBot(BOT_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

def findmes(m):
    chat = grpcmd(m, "find")
    if chat == "" :
        bot.send_message(m.chat.id, text = """Pls Send the Command with Valid Queries !!
        \n*To Search for VTube Content :-*
        Send /find `<search_query>`
        """, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        query = grpcmd(m, "find")
        try:
            telegraph = Telegraph()

            telegraph_res = telegraph.create_page(
                    short_name="VTube",
                    author_name='VTube Manager Bot',
                    author_url='https://t.me/VTube_Movies'
                )

            search_results = bot.send_message(m.chat.id, "`Searching in VTube ...`\n\n`Query` : *{}*".format(query), parse_mode=telegram.ParseMode.MARKDOWN)

            url_conf = "https://{}/api/v1/config?secret={}".format(LD_DOMAIN, SECRET)

            r1 = requests.get(url_conf)
            res1 = r1.json()
            search_acc_auth = res1["content"]["account_list"][0]["auth"]

            url_meta = "https://{}/api/v1/metadata?a={}&q={}".format(LD_DOMAIN, search_acc_auth, query)

            r2 = requests.get(url_meta)
            res2 = r2.json()

            html_string = ""
            num_of_results = 0

            if res2["code"] == 200 and res2["success"] == True:
                for cat in res2["content"]:
                    if len(cat["children"]) != 0:
                        for media in cat["children"]:
                            num_of_results += 1
                            title = media["title"]
                            type_ = cat["categoryInfo"]["type"]
                            if "releaseDate" in media.keys():
                                releaseDate = media["releaseDate"]
                            else:
                                releaseDate = ""
                            if "backdropPath" in media.keys():
                                backdrop = media["backdropPath"]
                            else:
                                backdrop = ""
                            if "overview" in media.keys():
                                overview = media["overview"]
                            else:
                                overview = ""

                            
                            if str(type_) == "TV Shows":
                                url_show = "intent:https://{}/view/{}#Intent;package={};S.title=@Tube_Movirs {};end".format(LD_DOMAIN, media["id"], APP_INTENT, media["title"])
                                f_html = "<b> - View Link : </b> <a href={}>Play/Download In VTube App.</a> \nLogIn Required!<br>".format(url_show)
                            else:
                                url_mov = "intent:https://{}/view/{}#Intent;package={};S.title=@Tube_Movirs {};end".format(LD_DOMAIN, media["id"], APP_INTENT, media["title"])
                                f_html = "<b> - View Link : </b><a href={}>Play/Download In VTube App.</a> \nLogIn Required!!!<br>".format(url_mov)
                            TG_html = '''<p>
                                            <img src=''' + str(backdrop) + '''>
                                            <b>Name : </b><code>''' + str(title) + '''</code><br>
                                            <b> - Overview : </b><code>''' + str(overview) + '''</code><br>
                                            <b> - Release Date : </b><code>''' + str(releaseDate) + '''</code><br>
                                            <b> - Type : </b><code>''' + str(type_) + '''</code><br>
                                            {}<br>➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖<br>
                                        </p>'''.format(f_html)

                            html_string = html_string + TG_html
                    else:
                        continue
            else:
                pass

            if num_of_results != 0:
                telegraph_res = telegraph.create_page(
                    title="VTube Search Results",
                    html_content=html_string,
                    author_name='VTube Manager Bot',
                    author_url='https://t.me/VTube_Movies'
                )

                telegraph_url = 'https://telegra.ph/{}'.format(telegraph_res['path'])
                keyboard = telebot.types.InlineKeyboardMarkup()
                keyboard.row(
                    telebot.types.InlineKeyboardButton("🔍Search Results", url=telegraph_url)
                )
                bot.edit_message_text("`Query` : *{}*\n`Found `*{}*` Matching Search Results !!`".format(query, str(num_of_results)), m.chat.id, message_id=search_results.message_id, reply_markup=keyboard, parse_mode=telegram.ParseMode.MARKDOWN)
            else:
                bot.edit_message_text("*No Matching Search Results !!*", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
        except:
            bot.edit_message_text("`VTube Manager Not Accessible To The Server!!`", m.chat.id, message_id=search_results.message_id, parse_mode=telegram.ParseMode.MARKDOWN)
