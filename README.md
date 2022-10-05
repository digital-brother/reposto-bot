This is guide how to setup this telegram bot

TELEGRAM BOT CREATION:
To create telegram bot, find @BotFather inside telegram, make sure this is official telegram bot it has "✓" near the name, after that click "start" button and type command /newbot to create new bot, do all what instruction said, in the end you will get HTTP API token, save it, you will need it later.
 
DJANGO PROJECT SETUP:
This project builded on python3.8. To run this project you need:
1. install "requirements.txt" to your virtual environment (pip install -r requirements.txt)
2. create  ".env" file inside project folder, near "manage.py" file, it has 3 fields:
    BOT_NAME=Botnameexample <-- This is name of your bot, it must be the same as in database
    SECRET_KEY=secretkeyexample <-- your Django secret key
    DEBUG=True <-- Django debug setting
3. run migrations with "python manage.py migrate"

DJANGO ADMIN EXPLANATION:
After you successfully run the server, the first page will be django admin, after login inside it you will see "Bots" and "Channels":
1. Bots:
    "Name" of the bot must be the same as "BOT_NAME" inside your ".env" file.
    "Token" this is your "HTTP API token" of the telegram bot.
2. Channels:
    "Bot" - this is bot that must work with this channel that you created
    "Telegram_id" - this is your channel's id inside telegram, you can get it by sending something to the @userinfobot, from your channel (like reposting some post    from channel to this telegram bot)
    "Username replacement" -- it must be filled in format ["@Exampleusr", "@Secondusr"] , the idea is, if @Exampleusr exist inside text of the message that posted in channel, it will swap with @Secondusr, after message will be reposted to the next channel
    "Promocode replacement" -- the logic is the same as with username, but it will swap promocode, format for word a bit different ["Promoexample1", "Promoexample2"]
    "External link" -- this can be any link that NOT a telegram link
    "Pin message link" -- this is link to telegram's message, this link allways must start with "https://t.me/"
    "Title" -- used only for better objects naming inside django admin, thats all.