# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-24 11:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scoreboard', '0002_auto_20170224_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='team0',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_team0', to='scoreboard.Team'),
        ),
        migrations.AlterField(
            model_name='event',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_team1', to='scoreboard.Team'),
        ),
    ]
