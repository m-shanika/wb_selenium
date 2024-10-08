# Generated by Django 5.1 on 2024-08-08 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session', models.TextField(verbose_name='Сессия')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Номер')),
                ('sex', models.CharField(choices=[('FEMALE', 'Female'), ('MALE', 'Male')], max_length=15, verbose_name='Пол')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('cookies', models.TextField(verbose_name='Куки')),
                ('token', models.TextField(verbose_name='Токен')),
                ('is_buy', models.BooleanField(default=False, verbose_name='Покупал')),
            ],
            options={
                'verbose_name': 'Аккаунт',
                'verbose_name_plural': 'Аккаунты',
            },
        ),
    ]
