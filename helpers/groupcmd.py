# CONFIG

from config import Config

BOT_TOKEN = Config.BOT_TOKEN
LD_DOMAIN = Config.LD_DOMAIN
SECRET = Config.SECRET
ADMIN_IDS = Config.ADMIN_IDS
GROUP_IDS = Config.GROUP_IDS
PIC = Config.PIC
HEROKU_API_KEY = Config.HEROKU_API_KEY
HEROKU_APP_NAME = Config.HEROKU_APP_NAME
SEARCH_AUTH = Config.SEARCH_AUTH
LD_DOMW = Config.LD_DOMW
APP_INTENT = Config.APP_INTENT
BOT_USERNAME = Config.BOT_USERNAME

def grpcmd(mes, cmd):
    if BOT_USERNAME in mes.text :
        query = mes.text.split(BOT_USERNAME)[1].strip()
    else:
        query = mes.text[(len(cmd)+2):]
    return query