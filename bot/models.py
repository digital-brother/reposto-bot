from django.core.exceptions import ValidationError
from django.db import models


class BotManager(models.Manager):
    def enabled(self):
        return self.filter(enabled=True)

    def active(self):
        return self.enabled().first()


class Bot(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

    objects = BotManager()

    def clean(self):
        model = self._meta.model
        enabled_bots_already_exists = model.objects.enabled().count() >= 1
        is_create = not self.pk
        if is_create and enabled_bots_already_exists:
            raise ValidationError('You already have a bot running. Disable it to enable another.')

    def __str__(self):
        return self.name


class Replacement(models.Model):
    from_text = models.CharField(max_length=128)
    to_text = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.from_text} - {self.to_text}"


class UsernameReplacement(Replacement):
    channel = models.ForeignKey('OutputChannel', related_name='username_replacements', on_delete=models.CASCADE)


class PromocodeReplacement(Replacement):
    channel = models.ForeignKey('OutputChannel', related_name='promocode_replacements', on_delete=models.CASCADE)


class Channel(models.Model):
    title = models.CharField(max_length=100)
    telegram_id = models.IntegerField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class OutputChannel(Channel):
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, related_name='repost_channels')
    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)


class InputChannel(Channel):
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, related_name='input_channels')

    def clean(self):
        is_create = not self.pk
        input_channel_already_exists = self.bot.input_channels.count() >= 1
        if is_create and input_channel_already_exists:
            raise ValidationError(f'You already have an input channel for {self.bot}. Delete it to create another.')
