# Generated by Django 4.0.4 on 2022-06-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AcmeChallenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('challenge', models.CharField(help_text='The identifier for this challenge', max_length=255, unique=True)),
                ('response', models.CharField(help_text='The response expected for this challenge', max_length=255)),
            ],
            options={
                'verbose_name': 'ACME Challenge',
                'verbose_name_plural': 'ACME Challenges',
            },
        ),
    ]