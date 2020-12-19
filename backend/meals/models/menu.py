from datetime import datetime as dt
from datetime import date
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model

from .abstract import AbstractMealsModel, MealsManager


User = get_user_model()


class MenuManager(MealsManager):

    def today(self):
        return self.filter(
            date=date.today())


class MenuModel(AbstractMealsModel):
    ''''''
    PLANNING = 0
    WAITING = 1
    DISPATCHED = 2
    STATUS_CHOICES = (
        (PLANNING, 'Planning the menu'),
        (WAITING, 'Waiting for preferences'),
        (DISPATCHED, 'Dispatched to employees'),
    )

    class NotCurrently(Exception):
        pass

    class NotAnnouncedYet(Exception):
        pass

    date = models.DateField(unique=True)
    plates = models.ManyToManyField(
        'PlateModel', related_name='in_menus')
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)
    announced = models.BooleanField(default=False)

    objects = MenuManager()

    def get_absolute_url(self):
        '''Get url for menu's detail view.

        :returns: (str) URL for user detail.
        '''
        return reverse('meals:menu-detail', args=[self.pk])

    @property
    def status_str(self):
        return self.STATUS_CHOICES[self.status][1]

    @property
    def current(self):
        return self.date == date.today()

    def out_of_limit(self, datetime=None):
        '''
        Indicates if the menu is out of bounds for selecting lunch
        preferences. If the menu does not correspond to the current
        day, it will return false.

        : parse datetime: (default = None) allows comparing with a
            datetime object other than the current time (for testing
            purposes).
        :return: boolean
        '''
        if not self.current:
            return True
        limit = settings.MEALS_PREFERENCE_LIMIT
        dtm = datetime if datetime else dt.now()
        limit = dt.strptime(
            f'{dt.strftime(dtm, "%Y-%m-%d ")}' + limit,
            '%Y-%m-%d %H:%M')
        return dtm > limit

    def close_preference(self):
        '''
        '''
        if not self.announced:
            raise self.NotAnnouncedYet
        if not self.current:
            raise self.NotCurrently
        self.status = self.DISPATCHED
        self.save()
