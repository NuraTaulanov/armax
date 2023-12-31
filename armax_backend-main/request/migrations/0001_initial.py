# Generated by Django 4.2 on 2023-09-30 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Полное имя')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='Электронная почта')),
                ('niche', models.SmallIntegerField(choices=[(1, 'Веб'), (2, 'Мобильное приложение'), (3, 'Десктопное приложение'), (4, 'Кроссплатформенное приложение')], default=1, verbose_name='Ниша')),
                ('project_desc', models.TextField(blank=True, null=True)),
                ('project_deadlines', models.TextField(blank=True, null=True)),
                ('project_budget', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
