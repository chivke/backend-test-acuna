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


def test_menumanager_today_url():
    menu = MenuModelFactory()
    menu.date = dt.date.today()
    menu.save()
    assert MenuModel.objects.today_url() == f'/menu/{menu.pk}/'


def test_menumodel_status_str():
    menu = MenuModelFactory()
    assert isinstance(menu.status, int)
    assert isinstance(menu.status_str, str)


def test_menumodel_current():
    menu = MenuModelFactory()
    menu.date = dt.date.today()
    menu.save()
    assert menu.current


def test_menumodel_announce():
    menu = MenuModelFactory()
    menu.date == dt.date.today() - dt.timedelta(1)
    try:
        menu.announce()
    except MenuModel.NotCurrently:
        raised = True
    assert raised


@pytest.fixture(autouse=True)
def test_menumodel_out_of_limit(settings):
    settings.MEALS_PREFERENCE_LIMIT = dt.datetime.strftime(
        dt.datetime.now() - dt.timedelta(hours=1), '%H:%M:%S')
    menu = MenuModelFactory()
    assert menu.out_of_limit()


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
