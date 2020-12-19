import uuid
from django.db import models
from django.utils import timezone


class MealsManager(models.Manager):
    '''
    Abstract manager to model of meals application.
    '''

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(
            *args, **kwargs).filter(deleted=False)


class AbstractMealsModel(models.Model):
    '''
    Abstract manager to model of meals application.
    '''
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(null=True)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True)

    objects = MealsManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        '''
        Registers latest edition.
        '''
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        '''
        Don't delete, just mark as deleted.
        '''
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
