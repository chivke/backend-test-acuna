import pytest
import datetime as dt
from backend.meals.models import MealModel, MenuModel
from backend.users.models import User
from django.utils import timezone
from .factories import MealModelFactory, MenuModelFactory, PlateModelFactory


pytestmark = pytest.mark.django_db


def test_abstract_model():
    meal = MealModelFactory()
    time = meal.modified_at
    assert not meal.deleted
    meal.delete()
    assert not MealModel.objects.filter(pk=meal.pk)
    assert meal.deleted
    assert time < meal.modified_at


def test_mealmanager_today():
    meal = MealModelFactory()
    meal.menu.date = dt.date.today()
    meal.menu.save()
    meal.save()
    assert meal == MealModel.objects.today().first()


def test_mealmanager_today_from_user(user: User):
    meal = MealModelFactory()
    meal.menu.date = dt.date.today()
    meal.employee = user
    meal.menu.save()
    meal.save()
    assert meal == MealModel.objects.today_from_user(user).first()


def test_menumanager_today():
    menu = MenuModelFactory()
    menu.date = dt.date.today()
    menu.save()
    assert menu == MenuModel.objects.today().first()


def test_menumodel_status_str():
    menu = MenuModelFactory()
    assert isinstance(menu.status, int)
    assert isinstance(menu.status_str, str)


def test_menumodel_current():
    menu = MenuModelFactory()
    menu.date = dt.date.today()
    menu.save()
    assert menu.current


def test_menumodel_out_of_limit():
    menu = MenuModelFactory()
    now = dt.datetime.now()
    menu.date = dt.date.today()
    menu.save()
    fake_now = dt.datetime(
        year=now.year, month=now.month, day=now.day, hour=10)
    fake_now_out = dt.datetime(
        year=now.year, month=now.month, day=now.day, hour=12)
    assert menu.out_of_limit(fake_now_out)
    assert not menu.out_of_limit(fake_now)


def test_menumodel_close_preference():
    menu = MenuModelFactory()
    try:
        menu.close_preference()
    except menu.NotAnnouncedYet:
        raised = True
    assert raised
    menu.announced = True
    menu.save()
    try:
        menu.close_preference()
    except menu.NotCurrently:
        raised = True
    assert raised
    menu.date = dt.date.today()
    menu.save()
    menu.close_preference()
    assert menu.status == menu.DISPATCHED


def test_platemodel_str():
    plate = PlateModelFactory()
    assert str(plate) == plate.short_desc


def test_platemodel_get_absolute_url():
    plate = PlateModelFactory()
    assert plate.get_absolute_url() == f'/nora/plate/{plate.pk}/'


def test_platemodel_record_usage():
    now = timezone.now()
    plate = PlateModelFactory()
    plate.record_usage()
    assert plate.last_use > now


def test_platemodel_times_eaten():
    meal = MealModelFactory()
    plate = meal.plate
    assert plate.times_eaten == 1


def test_platemodel_times_custom():
    meal = MealModelFactory()
    meal.customization = 'custom'
    meal.save()
    plate = meal.plate
    assert plate.times_custom == 1
