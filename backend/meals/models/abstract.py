import uuid
from django.db import models
from django.utils import timezone


class MealsManager(models.Manager):

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(
            *args, **kwargs).filter(deleted=False)


class AbstractMealsModel(models.Model):
    '''

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
        self.modified_at = timezone.now()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save()
