from django.core.management.base import BaseCommand
from django.conf import settings
import logging
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler

from bot.models import Bot, Channel

class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        token = Bot.objects.get(name=settings.BOT_NAME).token
        channels = []
        for channel in Channel.objects.all():
            channels.append(channel)
        
        async def start(update, context):
            await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


        async def repost(update, context):
            for channel in channels:
                if channel.telegram_id == update.effective_chat.id:
                    pass
                else:
                    print(update)
                    print('==========================')
                    message = update.channel_post.text
                    message += '123'
                    await context.bot.send_message(chat_id=channel.telegram_id, text=message)

        application = ApplicationBuilder().token(token).build()

        start_handler = CommandHandler('start', start)
        repost_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), repost)

        application.add_handler(start_handler)
        application.add_handler(repost_handler)

        application.run_polling()
