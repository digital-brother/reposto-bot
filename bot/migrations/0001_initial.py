# Generated by Django 4.1.1 on 2022-09-08 13:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='default_name', max_length=100)),
                ('enable', models.BooleanField(default=True)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='@default_name', max_length=100)),
                ('title', models.CharField(blank=True, default='default_title', max_length=100)),
                ('telegram_id', models.CharField(default='default_telegram_channel_id', max_length=100)),
                ('link', models.CharField(blank=True, default='default_link', max_length=100)),
                ('bot', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='channels', to='bot.bot')),
            ],
        ),
    ]
