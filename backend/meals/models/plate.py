from django.db import models
from django.utils import timezone
from .abstract import AbstractMealsModel
from django.urls import reverse


class PlateModel(AbstractMealsModel):
    '''
    Model of a meal plate.

    A plate is cooked and enjoyed more than once. A dish is cooked and
    enjoyed more than once. This model links the plate with the meals
    and the employees
    '''
    description = models.CharField(
        max_length=500, blank=True)
    short_desc = models.CharField(max_length=150)
    last_use = models.DateField(null=True)

    def __str__(self):
        return self.short_desc

    def get_absolute_url(self):
        '''Get url for plate's detail view.

        :returns: (str) URL for user detail.
        '''
        return reverse('meals:plate-update', args=[self.pk])

    def record_usage(self):
        '''
        Method to mark a use.
        '''
        self.last_use = timezone.now()
        self.save()

    @property
    def times_eaten(self):
        '''
        How many times the plate has been eaten.
        '''
        return self.meals.all().count()

    @property
    def times_custom(self):
        '''
        How many times the plate has been personalized.
        '''
        return self.meals.exclude(
            customization=None).count()
