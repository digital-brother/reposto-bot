from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import re
from telegram.ext import ApplicationBuilder, filters, MessageHandler

from bot.models import Bot, Channel


class Command(BaseCommand):

    def handle(self, *args, **options):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )
        enabled_bots = Bot.objects.filter(enabled=True)
        token = enabled_bots.get(name=settings.BOT_NAME).token

        channels = list(Channel.objects.all())

        external_link_regex = "(http(s?)://[a-zA-Z0-9./=?#-]+)"
        pin_link_regex = "(https://t.me/)"

        async def repost(update, context):
            for channel in channels:
                is_text_only = bool(update.channel_post.text_html)
                is_text_with_image = bool(update.channel_post.caption_html)

                if is_text_only:
                    message = update.channel_post.text_html.replace(
                        channel.username_replacement[0], channel.username_replacement[1]).replace(
                        channel.promocode_replacement[0], channel.promocode_replacement[1])
                    if re.search(external_link_regex, message) is not None:
                        if re.search(pin_link_regex, message):
                            message = message.replace(
                                re.search('(https://t.me/[a-zA-Z\d/]+)', message).group(), channel.pin_message_link
                                )
                        else:
                            message = message.replace(
                                re.search(external_link_regex, message).group(), channel.external_link
                                )
                    await context.bot.send_message(
                        chat_id=channel.telegram_id,
                        text=message,
                        parse_mode="HTML"
                        )

                elif is_text_with_image:
                    caption = update.channel_post.caption_html.replace(
                        channel.username_replacement[0], channel.username_replacement[1]).replace(
                        channel.promocode_replacement[0], channel.promocode_replacement[1])
                    if re.search(external_link_regex, caption) is not None:
                        if re.search(pin_link_regex, caption):
                            caption = caption.replace(
                                re.search('(https://t.me/[a-zA-Z\d/]+)', caption).group(), channel.pin_message_link
                                )
                        else:
                            caption = caption.replace(
                                re.search(external_link_regex, caption).group(), channel.external_link
                                )
                    await context.bot.copy_message(
                        chat_id=channel.telegram_id,
                        message_id=update.effective_message.id,
                        from_chat_id=update.effective_chat.id,
                        caption=caption,
                        parse_mode="HTML"
                        )

                else:
                    await context.bot.copy_message(
                        chat_id=channel.telegram_id,
                        message_id=update.effective_message.id,
                        from_chat_id=update.effective_chat.id
                        )

        application = ApplicationBuilder().token(token).build()
        repost_handler = MessageHandler(filters.ALL, repost)
        application.add_handler(repost_handler)
        application.run_polling()
