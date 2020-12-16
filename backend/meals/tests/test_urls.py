import pytest
from django.urls import resolve, reverse

from backend.meals.models import MealModel, MenuModel, PlateModel

from .factories import MenuModelFactory, PlateModelFactory

pytestmark = pytest.mark.django_db


def test_nora_url():
    assert reverse('meals:nora-view') == '/nora/'
    assert resolve('/nora/').view_name == 'meals:nora-view'


def test_nora_menu_create():
    assert reverse('meals:menu-create') == '/nora/menu/create/'
    assert resolve('/nora/menu/create/').view_name == 'meals:menu-create'


def test_nora_menu_update():
    menu = MenuModelFactory()
    assert (
        reverse('meals:menu-update', args=[menu.pk])
        == f'/nora/menu/{menu.pk}/'
    )
    assert resolve(f'/nora/menu/{menu.pk}/').view_name == 'meals:menu-update'


def test_nora_menu_delete():
    menu = MenuModelFactory()
    assert (
        reverse('meals:menu-delete', args=[menu.pk])
        == f'/nora/menu/{menu.pk}/delete/'
    )
    assert (
        resolve(f'/nora/menu/{menu.pk}/delete/').view_name
        == 'meals:menu-delete'
    )


def test_nora_plate_create():
    assert reverse('meals:menu-create') == '/nora/menu/create/'
    assert resolve('/nora/menu/create/').view_name == 'meals:menu-create'


def test_nora_plate_update():
    plate = PlateModelFactory()
    assert (
        reverse('meals:plate-update', args=[plate.pk])
        == f'/nora/plate/{plate.pk}/'
    )
    assert resolve(f'/nora/plate/{plate.pk}/').view_name == 'meals:plate-update'


def test_nora_plate_delete():
    plate = PlateModelFactory()
    assert (
        reverse('meals:plate-delete', args=[plate.pk])
        == f'/nora/plate/{plate.pk}/delete/'
    )
    assert (
        resolve(f'/nora/plate/{plate.pk}/delete/').view_name
        == 'meals:plate-delete'
    )


def test_nora_send_reminder():
    assert reverse('meals:send-reminder') == '/nora/send-reminder/'
    assert resolve('/nora/send-reminder/').view_name == 'meals:send-reminder'


def test_menu_preference():
    menu = MenuModelFactory()
    assert (
        reverse('meals:menu-preference', args=[menu.pk])
        == f'/menu/{menu.pk}/preference/'
    )
    assert (
        resolve(f'/menu/{menu.pk}/preference/').view_name
        == 'meals:menu-preference'
    )


def test_menu_detail():
    menu = MenuModelFactory()
    assert (
        reverse('meals:menu-detail', args=[menu.pk])
        == f'/menu/{menu.pk}/'
    )
    assert (
        resolve(f'/menu/{menu.pk}/').view_name
        == 'meals:menu-detail'
    )
