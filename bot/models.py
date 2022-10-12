from django.core.exceptions import ValidationError
from django.db import models


class SingleEnabledAllowedMixin:
    def clean(self):
        model = self._meta.model
        enabled_already_exists = model.objects.filter(enabled=True).exclude(pk=self.pk).count() >= 1
        if enabled_already_exists and self.enabled:
            raise ValidationError(f'You already have {model._meta.verbose_name} running. Disable it to enable another.')


class Bot(SingleEnabledAllowedMixin, models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

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
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, related_name='output_channels')
    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)


class InputChannel(SingleEnabledAllowedMixin, Channel):
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, related_name='input_channels')
    enabled = models.BooleanField(default=False)
