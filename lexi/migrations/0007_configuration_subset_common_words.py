# Generated by Django 3.0 on 2020-01-21 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexi', '0006_word_suggestions'),
    ]

    operations = [
        migrations.AddField(
            model_name='configuration',
            name='subset_common_words',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
    ]
