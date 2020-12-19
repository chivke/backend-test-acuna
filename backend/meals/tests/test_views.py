import pytest
import datetime as dt

from django.test import RequestFactory
from django.http import Http404
from django.urls import reverse
from django.db.models import QuerySet
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage import default_storage
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.messages import get_messages

from backend.meals.tests.factories import MenuModelFactory
from backend.users.tests.factories import UserFactory
from backend.users.models import User
from backend.meals.models import MenuModel
from backend.meals.views.common import RootRouterView
from backend.meals.views.employee import MenuPreferenceView, MenuView
from backend.meals.views.nora import SendReminderView, NoraView
from backend.meals.views.mixins import NoraRequiredMixin


pytestmark = pytest.mark.django_db


class TestRootRouterView:

    def test_redirect_employee(self, user: User, rf: RequestFactory):
        view = RootRouterView()
        request = rf.get('/fake-url/')
        request.user = user
        view.request = request
        assert view.get_redirect_url() == reverse('users:redirect')
        menu = MenuModelFactory()
        menu.date = dt.date.today()
        menu.save()
        assert view.get_redirect_url() == menu.get_absolute_url()

    def test_redirect_nora(self, rf: RequestFactory):
        view = RootRouterView()
        request = rf.get('/fake-url/')
        user = UserFactory()
        user.profile.role = user.profile.NORA
        user.profile.save()
        request.user = User.objects.filter(pk=user.pk).first()
        view.request = request
        assert view.get_redirect_url() == reverse('meals:nora-view')


class TestMenuPreferenceView:

    def test_dispatch(self, user: User, rf: RequestFactory):
        view = MenuPreferenceView()
        request = rf.get('/fake-url/')
        request.user = user
        view.request = request
        try:
            view.dispatch(request, 999)
        except Http404:
            raised = True
        assert raised
        menu = MenuModelFactory()
        now = dt.datetime.now()
        menu.date = dt.date.today()
        fake_now = dt.datetime(
            year=now.year, month=now.month, day=now.day, hour=12)
        try:
            view.dispatch(request, menu.pk, dt=fake_now)
        except Http404:
            raised = True
        assert raised
        menu.save()
        now = dt.datetime.now()
        fake_now = dt.datetime(
            year=now.year, month=now.month, day=now.day, hour=10)
        assert view.dispatch(request, menu.pk, dt=fake_now).status_code == 200

    def test_form_valid(self, user: User, rf: RequestFactory):
        view = MenuPreferenceView()
        request = rf.get('/fake-url/')
        request.user = user
        default_storage
        request.session = SessionStore()
        request._messages = default_storage(request)
        view.request = request
        menu = MenuModelFactory()
        form = MenuPreferenceView.form_class(data={
            'plate': menu.plates.first(),
            'customization': 'XXX'})
        assert form.is_valid()
        view.menu = menu
        response = view.form_valid(form)
        assert response.status_code == 302  # redirect
        assert response.url == reverse(
            'meals:menu-detail', args=[menu.pk])


class TestMenuView:

    def test_context_data(self, user: User, rf: RequestFactory):
        view = MenuView()
        request = rf.get('/fake-url/')
        request.user = AnonymousUser()
        view.request = request
        menu = MenuModelFactory()
        menu.date = dt.date.today()
        menu.save()
        view.kwargs = {'pk': menu.pk}
        view.object = view.get_object()
        context = view.get_context_data()
        assert context['today_date']
        assert not context.get('meal', False)
        request.user = user
        context = view.get_context_data()
        assert isinstance(context['meal'], QuerySet)


class TestNoraView:

    def test_get_context_data(self, rf: RequestFactory):
        user = UserFactory()
        user.profile.role = user.profile.NORA
        user.profile.save()

        request = rf.post('/meals/nora/create/')
        request.session = SessionStore()
        request._messages = default_storage(request)
        request.user = User.objects.filter(pk=user.pk).first()
        view = NoraView()
        view.request = request

        context = view.get_context_data()
        assert context['today']['menu'] is None
        assert isinstance(context['today']['out_of_limit'], bool)
        assert isinstance(context['today']['date'], dt.date)
        assert isinstance(context['today']['meals'], QuerySet)
        assert isinstance(context['today']['users_without_prefer'], QuerySet)
        assert context['today']['plates'] is None
        assert isinstance(context['all_menus'], QuerySet)
        assert isinstance(context['all_plates'], QuerySet)

        menu = MenuModelFactory()
        menu.date = dt.date.today()
        menu.save()
        context = view.get_context_data()
        assert isinstance(context['today']['menu'], MenuModel)
        assert isinstance(context['today']['plates'], QuerySet)


class TestSendReminderView:

    def test_post(self, rf: RequestFactory):
        user = UserFactory()
        user.profile.role = user.profile.NORA
        user.profile.save()

        request = rf.post('/meals/nora/create/')
        request.session = SessionStore()
        request._messages = default_storage(request)
        request.user = User.objects.filter(pk=user.pk).first()
        view = SendReminderView()
        view.request = request

        view.post(request)
        storage = [x for x in get_messages(request)]
        assert str(storage[-1]) == 'Not menu today'

        menu = MenuModelFactory()
        menu.date = dt.date.today()
        menu.status = menu.DISPATCHED
        menu.save()
        view.post(request)
        storage = [x for x in get_messages(request)]
        assert str(storage[-1]) == 'Menu is not currently'

        menu.status = menu.WAITING
        menu.save()
        view.post(request)
        storage = [x for x in get_messages(request)]
        assert str(storage[-1]) == 'Menu was announced'

        menu = MenuModel.objects.get(pk=menu.pk)  # reload
        assert menu.announced


class TestNoraRequiredMixin:

    def test_dispatch(self, rf: RequestFactory):
        view = NoraRequiredMixin()
        user = UserFactory()
        request = rf.post('/meals/nora/create/')
        request.session = SessionStore()
        request._messages = default_storage(request)
        request.user = user
        view.request = request
        try:
            view.dispatch(request)
        except PermissionDenied:
            raised = True
        assert raised
        user.profile.role = user.profile.NORA
        user.profile.save()
        try:
            view.dispatch(request)
        except AttributeError:  # because it is a mixin it does not have
            raised = True  # a dispatch method
        assert raised
