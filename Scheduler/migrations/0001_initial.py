# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('patient', models.CharField(max_length=255, verbose_name='Пациент')),
                ('reception_date', models.DateField(verbose_name='Дата приема')),
                ('reception_time', models.TimeField(verbose_name='Время приема')),
                ('doctor', models.ForeignKey(verbose_name='Доктор', to='Doctors.Doctor')),
            ],
        ),
    ]
