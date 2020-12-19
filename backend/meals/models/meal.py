from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from .abstract import AbstractMealsModel, MealsManager


User = get_user_model()


class MealManager(MealsManager):

    def today(self):
        return self.filter(menu__date=date.today())

    def today_from_user(self, user):
        '''
        '''
        return self.today().filter(employee=user)


class MealModel(AbstractMealsModel):
    '''
    '''
    employee = models.ForeignKey(
        'users.User',
        limit_choices_to={'role': 'E'},
        on_delete=models.PROTECT,
        related_name='meals')
    menu = models.ForeignKey(
        'MenuModel',
        on_delete=models.PROTECT,
        related_name='meals')
    plate = models.ForeignKey(
        'PlateModel',
        on_delete=models.PROTECT,
        related_name='meals',
        null=True)
    customization = models.TextField(
        blank=True, null=True)
    participated = models.BooleanField(default=False)

    objects = MealManager()
