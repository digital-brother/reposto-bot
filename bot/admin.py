from django.contrib import admin

from bot.models import Bot, OutputChannel, UsernameReplacement, PromocodeReplacement, InputChannel


class UsernameReplacementInline(admin.TabularInline):
    model = UsernameReplacement
    extra = 1


class PromocodeReplacementInline(admin.TabularInline):
    model = PromocodeReplacement
    extra = 1


class OutputChannelAdmin(admin.ModelAdmin):
    fields = ['title', 'telegram_id', 'external_link', 'pin_message_link']
    inlines = [
        UsernameReplacementInline,
        PromocodeReplacementInline
    ]


admin.site.register(Bot)
admin.site.register(InputChannel)
admin.site.register(OutputChannel, OutputChannelAdmin)
