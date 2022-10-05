from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Channel(models.Model):
    bot = models.ForeignKey(Bot, on_delete=models.DO_NOTHING, related_name='channels')
    telegram_id = models.IntegerField()
    title = models.CharField(max_length=100)  # Used for convenience in admin

    username_replacement = models.JSONField()
    promocode_replacement = models.JSONField()
    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.telegram_id
