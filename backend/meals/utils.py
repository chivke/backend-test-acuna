
import datetime as dt

from django.urls import reverse
from django.conf import settings

from celery.task.schedules import crontab


def cron_meals_preference_limit():
    '''
    It translates the cutoff time for selecting lunches set
    in variable MEALS_PREFERENCE_LIMIT and returns a crontab
    schema instance for celery.
    '''
    limit = dt.datetime.strptime(settings.MEALS_PREFERENCE_LIMIT, '%H:%M')
    return crontab(hour=limit.hour, minute=limit.minute)


def get_slack_reminder(menu, employee):
    '''
    Function that generates the message that is sent through slack
    along with the menu of the day and the dishes available.
    '''
    message = f'Hello {employee.username}!\n'\
              'I share with you today\'s menu :)\n'
    for idx, plate in enumerate(menu.plates.all()):
        message += f'Option {idx + 1}: {plate.short_desc}\n'
    message += 'Have a nice day!\n'
    message += reverse('meals:menu-detail', args=[menu.pk])
    return message
