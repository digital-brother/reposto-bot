# Generated by Django 4.1.1 on 2022-10-12 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0004_remove_repostchannel_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='inputchannel',
            name='telegram_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='inputchannel',
            name='title',
            field=models.CharField(default='a', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repostchannel',
            name='telegram_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repostchannel',
            name='title',
            field=models.CharField(default='a', max_length=100),
            preserve_default=False,
        ),
    ]
