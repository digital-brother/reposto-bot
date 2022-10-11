from django.contrib import admin

from bot.models import Bot, Channel, UsernameReplacement, PromocodeReplacement


class UsernameReplacementInline(admin.TabularInline):
    model = UsernameReplacement
    extra = 1


class PromocodeReplacementInline(admin.TabularInline):
    model = PromocodeReplacement
    extra = 1


class ChannelAdmin(admin.ModelAdmin):
    inlines = [
        UsernameReplacementInline,
        PromocodeReplacementInline
    ]


admin.site.register(Bot)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(UsernameReplacement)
admin.site.register(PromocodeReplacement)
