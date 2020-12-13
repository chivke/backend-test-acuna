from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager


class Profile(models.Model):
    '''Profile for User model.'''

    NORA = 'N'
    EMPLOYEE = 'E'
    ROLE_CHOICES = (
        (NORA, 'User with role of Nora'),
        (EMPLOYEE, 'Cornershop employee user')
    )

    #: determines the type of user
    role = models.CharField(
        'role', max_length=1,
        choices=ROLE_CHOICES)
    #: determines the owner user
    user = models.OneToOneField(
        'User', on_delete=models.CASCADE,
        related_name='profile')

    class Meta:
        verbose_name = 'profile'
        verbose_name_plural = 'profiles'

    def __str__(self):
        return f'{self.user.username} <{self.role}>'


class UserManager(UserManager):
    '''Model manager who creates profile when creating users.'''

    def create(self, role='E', *args, **kwargs):
        user = super().create(*args, **kwargs)
        user.create_profile(role=role)
        return user

    def get_or_create(self, role='E', *args, **kwargs):
        user, created = super().get_or_create(*args, **kwargs)
        user.create_profile(role=role)
        return user, created


class User(AbstractUser):
    '''Default user for nora's backend.'''

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    objects = UserManager()

    def __str__(self):
        '''Print profile if has it'''
        try:
            string = self.profile
        except User.profile.RelatedObjectDoesNotExist:
            string = self.username
        return f'{string}'

    def get_absolute_url(self):
        '''Get url for user's detail view.

        :returns: (str) URL for user detail.
        '''
        return reverse('users:detail', kwargs={'username': self.username})

    def create_profile(self, *args, **kwargs):
        '''Create a user profile

        :params: accept args & kwargs to .objects.create method.
        :returns: profile instance.
        '''
        profile, created = Profile.objects.get_or_create(
            user=self, *args, **kwargs)
        return profile
