'''common views for meals app'''

from django.views.generic import RedirectView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from backend.meals.models import MenuModel


class RootRouterView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.profile.is_nora:
            return reverse('meals:nora-view')
        else:
            return MenuModel.objects.today_url()


root_view = RootRouterView.as_view()
