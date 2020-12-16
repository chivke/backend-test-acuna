from datetime import datetime as dt
from datetime import date
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.conf import settings

from .abstract import AbstractMealsModel, MealsManager
from backend.meals.tasks import announce_menu_in_slacks


class MenuManager(MealsManager):

    def today(self):
        return self.filter(
            date=date.today())

    def today_url(self):
        return self.today().first().get_absolute_url()


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

    def announce(self):
        '''
        Change status to waiting (1) and announce it via slack.
        '''
        if self.current:
            if self.status > self.WAITING:
                raise self.NotCurrently
            employees = User.objects.with_slack()
            for employee in employees:
                self.announce_menu_in_slack(
                    self.pk, employee.pk)
            return None
        raise self.NotCurrently

    def out_of_limit(self):
        '''
        '''
        limit = settings.MEALS_PREFERENCE_LIMIT
        now = dt.now()
        limit = dt.strptime(
            f'{dt.strftime(now, "%Y-%m-%d ")}' + limit,
            '%Y-%m-%d %H:%M:%S')
        return now > limit

    def close_preference(self):
        '''
        '''
        if not self.announced:
            raise self.NotAnnouncedYet
        if not self.current:
            raise self.NotCurrently
        self.status == self.DISPATCHED
        self.save()
