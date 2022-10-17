from django.core.exceptions import ValidationError
from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BotChannelBinding(models.Model):
    bot = models.ForeignKey('Bot', related_name='channel_bindings', on_delete=models.PROTECT)
    input_channel = models.ForeignKey('InputChannel', on_delete=models.PROTECT)
    output_channels = models.ManyToManyField('OutputChannel')

    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.bot} - {self.input_channel}"

    def clean(self):
        model = self._meta.model
        bot_channel_bindings = model.objects.filter(bot=self.bot).exclude(pk=self.pk)

        duplicate_input_channel_bindings = bot_channel_bindings.filter(input_channel=self.input_channel)
        if duplicate_input_channel_bindings:
            raise ValidationError("Duplicate input channel binding")


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
    channel = models.ForeignKey('BotChannelBinding', related_name='username_replacements', on_delete=models.PROTECT)


class PromocodeReplacement(Replacement):
    channel = models.ForeignKey('BotChannelBinding', related_name='promocode_replacements', on_delete=models.PROTECT)
