from django.core.exceptions import ValidationError
from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def clean(self):
        enabled_bot_exists = Bot.objects.filter(enabled=True).exclude(pk=self.pk).exists()
        if enabled_bot_exists and self.enabled:
            raise ValidationError('Only single bot can be enabled. Disable this or a currently running bot.')


class BotChannelBinding(models.Model):
    bot = models.ForeignKey('Bot', related_name='channel_bindings', on_delete=models.PROTECT)
    input_channel = models.ForeignKey('InputChannel', on_delete=models.CASCADE)
    output_channel = models.ForeignKey('OutputChannel', on_delete=models.CASCADE)
    enabled = models.BooleanField(default=True)

    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ['bot', 'input_channel', 'output_channel']

    def __str__(self):
        return f"{self.input_channel} -> {self.output_channel}"


class Replacement(models.Model):
    from_text = models.CharField(max_length=128)
    to_text = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.from_text} - {self.to_text}"


class Channel(models.Model):
    title = models.CharField(max_length=100)
    telegram_id = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class InputChannel(Channel):
    pass


class OutputChannel(Channel):
    pass


class UsernameReplacement(Replacement):
    channel = models.ForeignKey('BotChannelBinding', related_name='username_replacements', on_delete=models.CASCADE)


class PromocodeReplacement(Replacement):
    channel = models.ForeignKey('BotChannelBinding', related_name='promocode_replacements', on_delete=models.CASCADE)
