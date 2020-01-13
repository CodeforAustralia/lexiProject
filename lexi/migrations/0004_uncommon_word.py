# Generated by Django 3.0 on 2020-01-13 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexi', '0003_configuration'),
    ]

    operations = [
        migrations.CreateModel(
            name='Uncommon_Word',
            fields=[
                ('word', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('is_common', models.BooleanField(default=False)),
                ('is_business_word', models.BooleanField(default=False)),
                ('creation_datetime', models.DateTimeField(auto_now_add=True)),
                ('creation_user', models.CharField(default='admin', max_length=20)),
            ],
        ),
    ]