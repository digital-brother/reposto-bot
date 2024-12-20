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
    list_display = ['id', 'input_channel', 'output_channel', 'input_channel_id', 'output_channel_id', 'bot',
                    'enabled']

    def input_channel_id(self, obj):
        return obj.input_channel.id if obj.input_channel else None

    def output_channel_id(self, obj):
        return obj.output_channel.id if obj.output_channel else None


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
