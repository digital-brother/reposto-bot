from django.core.management.base import BaseCommand
from django.conf import settings
import logging
import re
from telegram.ext import ApplicationBuilder, filters, MessageHandler

from bot.models import Bot, Channel


async def repost(update, context):
    channels = Channel.objects.all()
    async for channel in channels:
        is_text_only = bool(update.channel_post.text_html)
        is_text_with_image = bool(update.channel_post.caption_html)

        if is_text_only:
            work_content = update.channel_post.text_html
        elif is_text_with_image:
            work_content = update.channel_post.caption_html
        else:
            work_content = None

        if is_text_only:
            content = update_content(channel, work_content)
            await context.bot.send_message(
                chat_id=channel.telegram_id,
                text=content,
                parse_mode="HTML"
            )

        elif is_text_with_image:
            content = update_content(channel, work_content)
            await context.bot.copy_message(
                chat_id=channel.telegram_id,
                message_id=update.effective_message.id,
                from_chat_id=update.effective_chat.id,
                caption=content,
                parse_mode="HTML"
            )

        else:
            await context.bot.copy_message(
                chat_id=channel.telegram_id,
                message_id=update.effective_message.id,
                from_chat_id=update.effective_chat.id
            )


def update_content(channel, work_content):
    external_link_regex = "(http(s?)://[a-zA-Z0-9./=?#-]+)"
    pin_link_regex = "(https://t.me/)"

    content = work_content
    for username_replacement in channel.username_replacements.all():
        content = work_content.replace(f"@{username_replacement.from_text}", f"@{username_replacement.to_text}")

    for promocode_replacement in channel.promocode_replacements.all():
            content = content.replace(promocode_replacement.from_text, promocode_replacement.to_text)

    if re.search(external_link_regex, content) is not None:
        if re.search(pin_link_regex, content):
            content = content.replace(
                re.search('(https://t.me/[a-zA-Z\d/]+)', content).group(), channel.pin_message_link
            )
        else:
            content = content.replace(
                re.search(external_link_regex, content).group(), channel.external_link
            )
    return content


def run_bot():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    enabled_bots = Bot.objects.filter(enabled=True)
    token = enabled_bots.get(name=settings.BOT_NAME).token

    application = ApplicationBuilder().token(token).build()
    repost_handler = MessageHandler(filters.ALL, repost)
    application.add_handler(repost_handler)
    application.run_polling()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_bot()
