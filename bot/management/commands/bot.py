from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand
import logging
import re
from telegram.ext import ApplicationBuilder, filters, MessageHandler

from bot.models import Bot, BotChannelBinding, OutputChannel


async def repost(update, context):
    bot = await Bot.objects.filter(enabled=True).afirst()
    input_channel_telegram_id = update.channel_post.chat_id
    channel_bindings = BotChannelBinding.objects.filter(
        bot=bot, input_channel_id__telegram_id=input_channel_telegram_id, enabled=True)

    async for channel_binding in channel_bindings:
        is_text_only = bool(update.channel_post.text_html)
        is_text_with_image = bool(update.channel_post.caption_html)


        if is_text_only:
            work_content = update.channel_post.text_html
            inline_keyboard = update.channel_post.reply_markup
        elif is_text_with_image:
            work_content = update.channel_post.caption_html
            inline_keyboard = update.channel_post.reply_markup
        else:
            work_content = None

        output_channel = await OutputChannel.objects.aget(pk=channel_binding.output_channel_id)
        if is_text_only:
            content = await sync_to_async(update_content)(channel_binding, work_content)
            await context.bot.send_message(
                chat_id=output_channel.telegram_id,
                text=content,
                parse_mode="HTML",
                reply_markup=inline_keyboard
            )

        elif is_text_with_image:
            content = await sync_to_async(update_content)(channel_binding, work_content)
            await context.bot.copy_message(
                chat_id=output_channel.telegram_id,
                message_id=update.effective_message.id,
                from_chat_id=update.effective_chat.id,
                caption=content,
                parse_mode="HTML"
            )

        else:
            await context.bot.copy_message(
                chat_id=output_channel.telegram_id,
                message_id=update.effective_message.id,
                from_chat_id=update.effective_chat.id
            )


def update_content(channel, work_content):
    external_link_regex = r"(https?://(?!t.me)[a-zA-Z0-9./=?#-]+)"
    pin_link_regex = r"(https://t.me/[a-zA-Z\d/]+)"

    content = work_content
    for username_replacement in channel.username_replacements.all():
        content = content.replace(f"@{username_replacement.from_text}", f"@{username_replacement.to_text}")

    for promocode_replacement in channel.promocode_replacements.all():
            ignorecase_pattern = re.compile(promocode_replacement.from_text, re.IGNORECASE)
            content = ignorecase_pattern.sub(promocode_replacement.to_text, content)

    pin_links = re.findall(pin_link_regex, content)
    for pin_link in pin_links:
        content = content.replace(pin_link, channel.pin_message_link)

    external_links = re.findall(external_link_regex, content)
    for external_link in external_links:
        content = content.replace(external_link, channel.external_link)

    return content


def run_bot():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    bots = Bot.objects.filter(enabled=True)
    applications = []
    for bot in bots:
        application = ApplicationBuilder().token(bot.token).build()
        repost_handler = MessageHandler(filters.ALL, repost)
        application.add_handler(repost_handler)
        application.run_polling()
        applications.append(application)


class Command(BaseCommand):
    def handle(self, *args, **options):
        run_bot()


# TODO: Add case insensitive replacement for promocode
# TODO: Handle button repost
