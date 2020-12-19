import pytest

from celery.task.schedules import crontab

from backend.users.models import User
from backend.meals import utils

from .factories import MenuModelFactory


pytestmark = pytest.mark.django_db


def test_cron_meals_preference_limit():
    result = utils.cron_meals_preference_limit()
    assert isinstance(result, crontab)


def test_get_slack_reminder(user: User):
    menu = MenuModelFactory()
    msg = utils.get_slack_reminder(menu, user)
    assert isinstance(msg, str)
