from datetime import date
from django.db import models
from django.contrib.auth import get_user_model
from .abstract import AbstractMealsModel, MealsManager


User = get_user_model()


class MealManager(MealsManager):
    '''
    Manager to meal model.
    '''

    def today(self):
        '''
        Returns only the meals of today
        '''
        return self.filter(menu__date=date.today())

    def today_from_user(self, user):
        '''
        Return onlu the meals of today from user.
        '''
        return self.today().filter(employee=user)


class MealModel(AbstractMealsModel):
    '''
    Model of an employee meal.

    It links the employee, the menu, the dish ordered or
    assigned to him and the customization if required.
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
