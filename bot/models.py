from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100, default='default_name')
    enable = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Channel(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, default=None, related_name='channels')
    title = models.CharField(max_length=100, blank=True, default='default')
    telegram_id = models.IntegerField()

    username_replacement = models.JSONField(default=list)
    promocode_replacement = models.JSONField(default=list)
    external_link = models.CharField(max_length=100, blank=True, default='default')
    pin_message_link = models.CharField(max_length=100, blank=True, default='default')

    def __str__(self):
        return self.title
