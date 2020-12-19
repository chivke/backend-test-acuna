import random
from django.db import transaction
from django.conf import settings
from django.contrib.auth import get_user_model

from celery.utils.log import get_task_logger

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from config import celery_app

from backend.meals.models import MealModel, MenuModel
from backend.meals.utils import (
    get_slack_reminder,
    cron_meals_preference_limit)


User = get_user_model()
logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    '''
    '''
    sender.add_periodic_task(
        cron_meals_preference_limit(),
        menu_limit_and_dispatch.s())


@celery_app.task()
def menu_limit_and_dispatch():
    '''
    '''
    today_menu = MenuModel.objects.today().first()
    if not today_menu:
        logger.error('There is no menu to dispatch')
        return 1
    with transaction.atomic():
        for user in User.objects.filter(profile__role='E'):
            meal, created = MealModel.objects.get_or_create(
                employee=user, menu=today_menu)
            if not created and meal.participated:
                continue
            meal.plate = random.choice(today_menu.plates.all())
            meal.participated = False
            meal.save()
        today_menu.close_preference()
    return 0


def menu_announce_trigger(menu):
    '''
    Change status to waiting (1) and announce it via slack.
    '''
    if menu.current:
        if menu.status > menu.WAITING:
            raise menu.NotCurrently
        employees = User.objects.with_slack()
        for employee in employees:
            menu_announce_in_slack.delay(menu.pk, employee.pk)
        menu.status = menu.WAITING
        menu.announced = True
        menu.save()
        return None

    raise menu.NotCurrently


@celery_app.task()
def menu_announce_in_slack(menu_pk, employee_pk):
    '''
    '''
    menu = MenuModel.objects.filter(pk=menu_pk).first()
    employee = User.objects.filter(pk=employee_pk).first()
    if not menu or not employee:
        logger.error('primary key of menu or employee not exist')
        return 1

    slack_client = WebClient(token=settings.SLACK_BOT_TOKEN)
    try:
        response = slack_client.chat_postMessage(
            channel=employee.profile.slack_id,
            text=get_slack_reminder(menu, employee))
    except SlackApiError as e:
        logger.error(f'Slack error:{e}')
        return 1
    assert response['ok']
    return 0
