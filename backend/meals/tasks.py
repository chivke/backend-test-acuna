import os

from django.urls import reverse
from django.config import settings
from django.contrib.auth import forms, get_user_model

from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import celery_app
from backend.meals.models import MenuModel


User = get_user_model()
logger = get_task_logger(__name__)


def get_slack_reminder(menu, employee):
    '''
    '''
    message = 'Hello {employee.first_name}!\n'\
              'I share with you today\'s menu :)\n'
    for idx, plate in enumerate(menu):
        message += f'Option {idx}: {plate.short_desc}\n'
    message += 'Have a nice day!\n'
    message += reverse('meals:menu-detail', args=[menu.pk])


@celery_app.task()
def announce_menu_in_slack(menu_pk, employee_pk):
    '''
    '''
    menu = MenuModel.objects.filter(pk=menu_pk).first()
    employee = User.objects.filter(pk=employee_pk).first()
    if not menu or not employee:
        logger.error('primary key of menu or employee not exist')
        return None

    slack_client = WebClient(token=settings['SLACK_BOT_TOKEN'])
    try:
        response = slack_client.chat_postMessage(
            channel=employee.slack_id,
            text=get_slack_reminder(menu, employee))
    except SlackApiError as e:
        logger.error(f'Slack error:{e}')
