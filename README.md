This is guide how to set up a telegram bot

### Overview:
The project aim is to repost all messages from a Telegram channel to another channels.

Consists of 2 parts:
- Django - needed to configure bot, save config to DB
- Management command - runs the bot, reads config from DB

### Telegram bot creation:
1. find @BotFather inside Telegram, make sure that it is an official telegram bot it has "✓" near the name
2. click "start" button
3. type command `/newbot` to create a new bot, execute further Telegram instructions
4. in the end you will get HTTP API token, save it, you will need it later
 
### Django project setup:
This project is build with python3.8. To run this project you need:
1. install "requirements.txt" to your virtual environment `pip install -r requirements.txt`
2. create  ".env" file inside a project folder, near "manage.py" file, it has 3 fields:
   - BOT_NAME=Botnameexample <-- This is name of your bot, it must be the same as in database
   - SECRET_KEY=secretkeyexample <-- your Django secret key
   - DEBUG=True <-- Django debug setting
3. run migrations `python manage.py migrate`
4. create a superuser `python manage.py createsuperuser`

### Django admin explanation:
After you successfully run the server, the first page will be django admin, after login inside it you will see "Bots" and "Channels":
1. Bots:    
    - "Name" of the bot must be the same as "BOT_NAME" inside your ".env" file.
    - "Token" this is your "HTTP API token" of the telegram bot.
2. Channels:
  - "Title" -- used only for better objects naming inside django admin, thats all.
  - "Telegram_id" - this is your channel's id inside telegram, 
     - forward a message to the @userinfobot, from your channel to repost
     - copy forward_from_chat.id value
3. Channel bindings:
   - "Bot" - this is bot that must work with this channel that you created
   - "Username replacement" -- it must be filled in format ["@Exampleusr", "@Secondusr"] , the idea is, if @Exampleusr exist inside text of the message that posted in channel, it will swap with @Secondusr, after message will be reposted to the next channel
   - "Promocode replacement" -- the logic is the same as with username, but it will swap promocode, format for word a bit different ["Promoexample1", "Promoexample2"]
   - "External link" -- this can be any link that NOT a telegram link
   - "Pin message link" -- this is link to telegram's message, this link allways must start with "https://t.me/"
   