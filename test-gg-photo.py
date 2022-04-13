import pickle
import redis
import os, random
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from google.auth.transport.requests import Request
from telegram.ext import Updater ,CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ParseMode, ReplyKeyboardMarkup
from yaml import Loader, load

with open("./secret.yaml","r") as yml_file:
    data = load(yml_file, Loader=Loader)

# connect redis
HOST = data["redis"]["host"]
PASSWORD = data["redis"]["pass"]
redis_server = redis.Redis(host=HOST, port=6379, db=1, password=PASSWORD)
all_keys = redis_server.keys()

def get_all_key_redis():
    all_keys = redis_server.keys()
    all_keys = [key.decode("utf-8") for key in all_keys]
    # print(all_keys)
    return all_keys

reply_keboard = [['/girl','/woman'],['/vsbg','/sexygirl'],['/korean','/gaitay']]
markup = ReplyKeyboardMarkup(reply_keboard,one_time_keyboard=True)

def save_in_redis(d_value):
    print(type(d_value))
    # valuee = json.dumps(d_value,indent=2).encode("utf-8")
    # valuee = json.dumps(d_value)
    # value = {"value":valuee}

    try:
        with redis_server.pipeline() as pipe:
            # save key in redis
            pipe.set("girl",d_value)
            # expire key
            pipe.expire(86400)
            pipe.execute()
        redis_server.bgsave()
    except Exception as e:
        print(e)
    print("save done")

# def get_value_redis(str_key):
#     d_b_value = redis_server.hgetall(str_key)
#     d_value = {k.decode("utf-8"):v.decode("utf-8") for k,v in d_b_value.items()}
#     return d_value

def get_data_redis():
    # d_b_value = redis_server.hgetall(str_key)
    s_b_value = redis_server.get(str_key)
    s_value = s_b_value.decode("utf-8")
    l_value = json.loads(s_value)
    return l_value

def get_google_album():
    print("get image from gg")
    scopes = ['https://www.googleapis.com/auth/photoslibrary.readonly']

    creds = None
    CREDENTIALS_FILE = 'credentials.pickle'

    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                scopes)
            creds = flow.run_local_server(port=8090)
            with open(CREDENTIALS_FILE, 'wb') as token:
                pickle.dump(creds, token)

    service = build('photoslibrary', 'v1', credentials=creds,static_discovery=False)

    albums_shared = service.sharedAlbums().list(
        pageSize=10).execute()

    list_album = albums_shared.get('sharedAlbums', [])
    # print(list_album)
    for album in list_album:
        if album["title"] == "gái xinh":
            album_id = album["id"]

    nextpagetoken = 'Dummy'
    c=0
    list_item=[]
    while nextpagetoken != '':
        print("wait.....")
        nextpagetoken = '' if nextpagetoken == 'Dummy' else nextpagetoken
        results = service.mediaItems().search(
                body={"albumId": album_id,
                    "pageSize": 100, "pageToken": nextpagetoken}).execute()
        # The default number of media items to return at a time is 25. The maximum pageSize is 100.
        items = results.get('mediaItems', [])
        nextpagetoken = results.get('nextPageToken', '')
        for item in items:
            c+=1
            print(f"{c}\nURL: {item['productUrl']}")
            list_item.append(item['baseUrl'])
            # l.append(item['productUrl'])
    return list_item


def get_girl_img():
    print("check redis first")
    list_keys = get_all_key_redis()
    if list_keys == []:
        l_img = get_google_album()
        img = random.choice(l_img)
        print("gg",img)
        s_l_img = json.dumps(l_img)
        save_in_redis(s_l_img)
    else:
        l_img = get_data_redis()
        img = random.choice(l_img)
        print("redis",img)
    return img

def start(bot,update):
    user = update.message.from_user
    update.message.reply_text(
        "Hello master {} \nType /gái /sexygirl /girl /lady /vsbg /woman /korean /gaitay to see random picture\nHave fun :)".format(user.full_name),
        reply_markup=markup)

def help(bot,update):
    update.message.reply_text('''Note:
    /gái /girl /lady /woman: _Gái xinh chọn lọc_
    /sexygirl /vsbg : _Gái xinh quyến rũ_
    /korean /korea /gáihàn: _Gái Hàn Xẻng_
    /gaitay /gáitây: _Gái Tây_
    *Have fun* :) ''',ParseMode.MARKDOWN)

def girl(bot,update):
    girl = get_girl_img()
    chat_id = update.message.chat_id
    mess_id = update.message.message_id
    bot.send_photo(chat_id=chat_id,reply_to_message_id=mess_id, photo=girl)

def main():
    tele_TOKEN = data["telegram"]["token_quote"]
    updater = Updater(tele_TOKEN)
    
    dp = updater.dispatcher
    start_handler = CommandHandler('start',start)
    dp.add_handler(CommandHandler('help',help))
    dp.add_handler(CommandHandler(['girl','gái','women','lady'],girl))

    dp.add_handler(start_handler)
    #start the bot
    updater.start_polling()
    #Run the bot until press ctrl +C
    updater.idle()
    
if __name__ == '__main__':
    main()