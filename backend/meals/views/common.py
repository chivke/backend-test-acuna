'''common views for meals app'''

from django.views.generic import RedirectView
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin

from backend.meals.models import MenuModel


class RootRouterView(LoginRequiredMixin, RedirectView):
    '''
    View that controls the root of the application and redirects in
    relation to whether the user is authenticated, is an employee or is Nora.
    '''

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.profile.is_nora:
            return reverse('meals:nora-view')
        else:
            menu = MenuModel.objects.today().first()
            if not menu:
                return reverse('users:redirect')
            return menu.get_absolute_url()


root_view = RootRouterView.as_view()
