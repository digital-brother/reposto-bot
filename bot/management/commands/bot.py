from django.core.management.base import BaseCommand
import logging
import re
from telegram.ext import ApplicationBuilder, filters, MessageHandler

from bot.models import Bot


async def repost(update, context):
    bot = await Bot.objects.filter(enabled=True).afirst()
    input_channel_id = update.channel_post.chat_id
    input_channel = await bot.input_channels.aget(telegram_id=input_channel_id)

    async for channel in input_channel.output_channels.all():
        is_text_only = bool(update.channel_post.text_html)
        is_text_with_image = bool(update.channel_post.caption_html)

        if is_text_only:
            work_content = update.channel_post.text_html
        elif is_text_with_image:
            work_content = update.channel_post.caption_html
        else:
            work_content = None

        if is_text_only:
            content = await update_content(channel, work_content)
            await context.bot.send_message(
                chat_id=channel.telegram_id,
                text=content,
                parse_mode="HTML"
            )

        elif is_text_with_image:
            content = await update_content(channel, work_content)
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


async def update_content(channel, work_content):
    external_link_regex = "(http(s?)://[a-zA-Z0-9./=?#-]+)"
    pin_link_regex = "(https://t.me/)"

    content = work_content
    async for username_replacement in channel.username_replacements.all():
        content = work_content.replace(f"@{username_replacement.from_text}", f"@{username_replacement.to_text}")

    async for promocode_replacement in channel.promocode_replacements.all():
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
    bot = Bot.objects.get(enabled=True)
    application = ApplicationBuilder().token(bot.token).build()
    repost_handler = MessageHandler(filters.ALL, repost)
    application.add_handler(repost_handler)
    application.run_polling()


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_bot()
