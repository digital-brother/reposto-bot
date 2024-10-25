from django.contrib import admin

from bot.models import Bot, OutputChannel, UsernameReplacement, PromocodeReplacement, InputChannel, BotChannelBinding


class UsernameReplacementInline(admin.TabularInline):
    model = UsernameReplacement
    extra = 1


class PromocodeReplacementInline(admin.TabularInline):
    model = PromocodeReplacement
    extra = 1


class BotChannelBindingAdmin(admin.ModelAdmin):
    model = BotChannelBinding
    inlines = [
        UsernameReplacementInline,
        PromocodeReplacementInline
    ]
    list_filter = ['bot']
    list_display = ['id', 'input_channel', 'output_channel', 'bot', 'enabled']


class InputChannelAdmin(admin.ModelAdmin):
    model = InputChannel
    list_display = ['__str__', 'telegram_id']


class OutputChannelAdmin(admin.ModelAdmin):
    model = OutputChannel
    list_display = ['__str__', 'telegram_id']


class BotAdmin(admin.ModelAdmin):
    model = Bot
    list_display = ['__str__', 'enabled']


admin.site.register(Bot, BotAdmin)
admin.site.register(InputChannel, InputChannelAdmin)
admin.site.register(OutputChannel, OutputChannelAdmin)
admin.site.register(BotChannelBinding, BotChannelBindingAdmin)
