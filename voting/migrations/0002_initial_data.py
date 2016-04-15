# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-15 22:15

## Program, který automaticky přidá data do databáze.
## Většinou takovouhle věc nebudeš potřebovat; kdyby jo, dokumentace je na
## https://docs.djangoproject.com/en/1.9/topics/migrations/

## Tenhle soubor doporučuju ze začátku přeskočit.


from __future__ import unicode_literals

from django.db import migrations, models


def add_initial_poll(apps, schema_editor):
    # We can't import the Person model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Poll = apps.get_model("voting", "Poll")
    Option = apps.get_model("voting", "Option")
    poll = Poll(title='Kdy dáme sraz?')
    poll.save()

    for title in '9. 4.', '16. 4.', '23. 4.', '28. 4.':
        option = Option(poll=poll, title=title)
        option.save()


class Migration(migrations.Migration):

    dependencies = [
        ('voting', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_initial_poll),
    ]