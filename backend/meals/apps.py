from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MealsConfig(AppConfig):
    name = 'backend.meals'
    verbose_name = _('Meals')

    def ready(self):
        try:
            import backend.users.signals  # noqa F401
        except ImportError:
            pass
