
import datetime
from django.http import Http404
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    TemplateView, CreateView, UpdateView, DeleteView, RedirectView)
from django.conf import settings
from django.contrib import messages

from backend.meals.models import MenuModel, PlateModel, MealModel
from backend.meals.forms import MenuForm, PlateForm
from backend.meals.tasks import menu_announce_trigger

from backend.users.models import User

from .mixins import NoraRequiredMixin


class NoraView(NoraRequiredMixin, TemplateView):
    '''
    '''
    template_name = 'meals/nora/main.html'
    extra_context = {'title': 'Nora\'s dashboard'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Nora\'s dashboard'
        today_menu = MenuModel.objects.today().first()
        context['today'] = {
            'menu': today_menu,
            'out_of_limit': today_menu.out_of_limit if today_menu else True,
            'date': datetime.date.today(),
            'meals': MealModel.objects.today(),
            'users_without_prefer': User.objects.filter(
                profile__role='E').exclude(
                    meals__menu__date=datetime.date.today()),
            'plates': today_menu.plates.all() if today_menu else None,
        }
        context['prefer_limit'] = settings.MEALS_PREFERENCE_LIMIT
        context['all_menus'] = MenuModel.objects.all()
        context['all_plates'] = PlateModel.objects.all()
        return context


nora_view = NoraView.as_view()


class SendReminderView(NoraRequiredMixin, RedirectView):

    def post(self, request, *args, **kwargs):
        today_menu = MenuModel.objects.today().first()
        if not today_menu:
            messages.add_message(
                request, messages.ERROR, 'Not menu today')
            return self.get(request, *args, **kwargs)
        try:
            menu_announce_trigger(today_menu)
        except MenuModel.NotCurrently:
            messages.add_message(
                request, messages.ERROR, 'Menu is not currently')
        else:
            messages.add_message(request, messages.INFO, 'Menu was announced')
        return self.get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse('meals:nora-view')


send_reminder_view = SendReminderView.as_view()


class CreateMenuView(NoraRequiredMixin, CreateView):
    '''
    '''
    model = MenuModel
    template_name = 'meals/nora/menu-create.html'
    extra_context = {'title': 'Create menu'}
    form_class = MenuForm


menu_create_view = CreateMenuView.as_view()


class UpdateMenuView(NoraRequiredMixin, UpdateView):
    '''
    '''
    model = MenuModel
    template_name = 'meals/nora/menu-update.html'
    extra_context = {'title': 'Update menu'}
    form_class = MenuForm


menu_update_view = UpdateMenuView.as_view()


class DeleteMenuView(NoraRequiredMixin, DeleteView):
    '''
    '''
    model = MenuModel
    template_name = 'meals/nora/delete.html'
    extra_context = {'aux': 'menu'}
    success_url = reverse_lazy('meals:nora-view')


menu_delete_view = DeleteMenuView.as_view()


class CreatePlateView(NoraRequiredMixin, CreateView):
    model = PlateModel
    template_name = 'meals/nora/plate-create.html'
    extra_context = {'title': 'Create plate'}
    form_class = PlateForm


plate_create_view = CreatePlateView.as_view()


class UpdatePlateView(NoraRequiredMixin, UpdateView):
    model = PlateModel
    template_name = 'meals/nora/plate-update.html'
    extra_context = {'title': 'Update plate'}
    form_class = PlateForm


plate_update_view = UpdatePlateView.as_view()


class DeletePlateView(NoraRequiredMixin, DeleteView):
    '''
    '''
    model = PlateModel
    template_name = 'meals/nora/delete.html'
    extra_context = {'aux': 'plate'}
    success_url = reverse_lazy('meals:nora-view')


plate_delete_view = DeletePlateView.as_view()
