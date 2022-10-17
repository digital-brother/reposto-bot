from django.db import models


class Bot(models.Model):
    name = models.CharField(max_length=100)
    enabled = models.BooleanField(default=True)
    token = models.CharField(max_length=100)
    input_channels = models.ManyToManyField('InputChannel', related_name='bots', blank=True)
    output_channels = models.ManyToManyField('OutputChannel', related_name='bots', blank=True)

    def __str__(self):
        return self.name


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
    external_link = models.CharField(max_length=100, blank=True)
    pin_message_link = models.CharField(max_length=100, blank=True)


class UsernameReplacement(Replacement):
    channel = models.ForeignKey('OutputChannel', related_name='username_replacements', on_delete=models.CASCADE)


class PromocodeReplacement(Replacement):
    channel = models.ForeignKey('OutputChannel', related_name='promocode_replacements', on_delete=models.CASCADE)
