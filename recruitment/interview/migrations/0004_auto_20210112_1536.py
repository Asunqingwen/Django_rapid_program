# Generated by Django 3.1.5 on 2021-01-12 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interview', '0003_auto_20210112_1414'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'permissions': [('export', 'Can export candidate list'), ('notify', 'notify interviewer for candidate review')], 'verbose_name': '应聘者', 'verbose_name_plural': '应聘者'},
        ),
    ]
