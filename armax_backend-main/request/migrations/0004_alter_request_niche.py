# Generated by Django 4.2 on 2023-10-03 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0003_alter_request_niche'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='niche',
            field=models.CharField(choices=[(1, 'Веб'), (2, 'Мобильное приложение'), (3, 'Десктопное приложение'), (4, 'Кроссплатформенное приложение')], default='Не указано', max_length=20, verbose_name='Ниша'),
        ),
    ]
