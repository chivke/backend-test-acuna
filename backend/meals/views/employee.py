from django.shortcuts import get_object_or_404
from datetime import date
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.contrib.messages.views import SuccessMessageMixin
from backend.meals.forms import MenuPreferenceForm
from backend.meals.models import MenuModel, MealModel


class MenuPreferenceView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'menu/preference.html'
    form_class = MenuPreferenceForm
    success_message = 'a "%(plate)"" plate was preferred'

    def dispatch(self, request, pk, *args, **kwargs):
        self.menu = get_object_or_404(MenuModel, pk=pk)
        if self.menu.out_of_limit:
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.employee = self.request.user
        form.instance.menu = self.menu
        form.instance.participated = True
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('meals:menu-detail', args=[self.menu.pk])

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(plate=self.object.plate.short_desc)


menu_preference_view = MenuPreferenceView.as_view()


class MenuView(DetailView):
    template_name = 'menu/detail.html'
    queryset = MenuModel.objects.today()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meal'] = MealModel.objects.today_from_user(
            self.request.user)
        context['today_date'] = date.today()
        return context


menu_detail_view = MenuView.as_view()
