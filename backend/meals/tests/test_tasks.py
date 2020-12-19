import pytest
import datetime as dt

from backend.meals.models import MealModel, MenuModel
from backend.meals.tests.factories import MenuModelFactory
from backend.users.tests.factories import UserFactory

from backend.meals.tasks import (
    menu_limit_and_dispatch,
    menu_announce_trigger,
    menu_announce_in_slack)


pytestmark = pytest.mark.django_db


def test_menu_limit_and_dispatch(settings):
    '''
    '''
    users = UserFactory.create_batch(3)
    settings.CELERY_TASK_ALWAYS_EAGER = True
    assert menu_limit_and_dispatch.delay().result == 1

    menu = MenuModelFactory()
    menu.date = dt.date.today()
    menu.announced = True
    menu.save()
    meal = MealModel.objects.create(
        employee=users[0], menu=menu, plate=menu.plates.first())
    meal.participated = True
    meal.save()
    assert menu_limit_and_dispatch.delay().result == 0
    assert MenuModel.objects.today().first() == menu
    assert MenuModel.objects.today().first().status == menu.DISPATCHED

    meals = MealModel.objects.today()
    assert meals.count() == 3


def test_menu_announce_trigger(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    user = UserFactory()
    assert menu_announce_in_slack.delay(0, user.pk).result == 1
    menu = MenuModelFactory()
    try:
        menu_announce_trigger(menu)
    except menu.NotCurrently:
        raised = True
    assert raised

    menu.date = dt.date.today()
    menu.save()
    user.profile.slack_id = 'XXX'
    user.profile.save()
    user.save()
    assert menu_announce_in_slack.delay(menu.pk, user.pk).result == 1

    user.profile.slack_id = settings.SLACK_TEST_USER_ID
    user.profile.save()
    user.save()
    assert menu_announce_in_slack.delay(menu.pk, user.pk).result == 0

    assert menu.status == menu.PLANNING
    menu_announce_trigger(menu)
    assert menu.status == menu.WAITING
    assert menu.announced
    menu.status = menu.DISPATCHED
    menu.save()
    try:
        menu_announce_trigger(menu)
    except menu.NotCurrently:
        raised = True
    assert raised


# def test_menu_announce_in_slack(settings):
#     settings.CELERY_TASK_ALWAYS_EAGER = True
#     user = UserFactory()
#     menu = MenuModelFactory()
#     user.profile.slack_id = settings.SLACK_TEST_USER_ID
#     user.profile.save()
#     user.save()
    
