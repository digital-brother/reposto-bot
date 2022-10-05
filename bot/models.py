from django.core.exceptions import ValidationError
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

    def clean(self):
        username_replacement_field_name = Channel.username_replacement.field.verbose_name.capitalize()
        self.clean_list_of_lists(self.username_replacement, username_replacement_field_name)

        promocode_replacement_field_name = Channel.promocode_replacement.field.verbose_name.capitalize()
        self.clean_list_of_lists(self.promocode_replacement, promocode_replacement_field_name)

    @staticmethod
    def clean_list_of_lists(content, field_name):
        if not isinstance(content, list):
            raise ValidationError(f"{field_name} should be a list")

        for item in content:
            if not isinstance(item, list):
                raise ValidationError(f"{field_name} should contain a list of lists: {item} is not a list")

            if not len(item) == 2:
                raise ValidationError(f"Each {field_name} item should contain exactly 2 elements: "
                                      f"{item} has invalid length")

    def __str__(self):
        return self.title
