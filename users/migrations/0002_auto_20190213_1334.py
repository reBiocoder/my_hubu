# Generated by Django 2.1.4 on 2019-02-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='nick_name',
            field=models.CharField(default='username', max_length=20, verbose_name='昵称'),
        ),
    ]
