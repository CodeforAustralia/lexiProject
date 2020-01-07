# Generated by Django 3.0 on 2020-01-07 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lexi', '0002_auto_20190924_1351'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(choices=[('TH', 'Thesaurus'), ('DB', 'Database'), ('AI', 'AI Model')], default='TH', max_length=2)),
                ('threshold', models.FloatField(default=0.8)),
            ],
        ),
    ]
