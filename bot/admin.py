from django.contrib import admin

from bot.models import Bot, Channel, UsernameReplacement, PromocodeReplacement


class UsernameReplacementInline(admin.TabularInline):
    model = UsernameReplacement


class PromocodeReplacementInline(admin.TabularInline):
    model = PromocodeReplacement


class ChannelAdmin(admin.ModelAdmin):
    inlines = [
        UsernameReplacementInline,
        PromocodeReplacementInline
    ]


admin.site.register(Bot)
admin.site.register(Channel, ChannelAdmin)
