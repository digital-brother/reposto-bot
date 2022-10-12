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
        enabled_bots_count = model.objects.enabled().count()
        is_create = not self.pk
        if is_create and enabled_bots_count >= 1:
            raise ValidationError('You already have a bot running. Disable it to enable another.')

    def __str__(self):
        return self.name


class RepostChannel(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, related_name='repost_channels')
    telegram_id = models.IntegerField()
    title = models.CharField(max_length=100)  # Used for convenience in admin

    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Replacement(models.Model):
    from_text = models.CharField(max_length=128)
    to_text = models.CharField(max_length=128)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.from_text} - {self.to_text}"


class UsernameReplacement(Replacement):
    channel = models.ForeignKey(RepostChannel, related_name='username_replacements', on_delete=models.CASCADE)


class PromocodeReplacement(Replacement):
    channel = models.ForeignKey(RepostChannel, related_name='promocode_replacements', on_delete=models.CASCADE)
