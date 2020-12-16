from factory import Faker, SubFactory, Sequence, post_generation
from factory.django import DjangoModelFactory

from backend.meals.models import MealModel, MenuModel, PlateModel

from backend.users.tests.factories import UserFactory


class PlateModelFactory(DjangoModelFactory):
    description = Faker('text')
    short_desc = Sequence(lambda n: 'plate %s' % n)
    last_use = Faker('date')

    class Meta:
        model = PlateModel


class MenuModelFactory(DjangoModelFactory):
    date = Faker('date')
    status = 0
    announced = False

    class Meta:
        model = MenuModel

    @post_generation
    def plates(self, create, extracted, **kwargs):
        if not create:
            return
        self.plates.add(PlateModelFactory())
        if extracted:
            for plate in extracted:
                self.plates.add(plate)


class MealModelFactory(DjangoModelFactory):
    employee = SubFactory(UserFactory)
    menu = SubFactory(MenuModelFactory)
    plate = SubFactory(PlateModelFactory)
    customization = Faker('text')
    participated = False

    class Meta:
        model = MealModel
