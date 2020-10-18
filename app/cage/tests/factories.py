from datetime import datetime, timedelta

from cage.models import Inmate, List, ListItem, Prison
from factory import LazyFunction, Sequence, SubFactory
from factory.django import DjangoModelFactory


class InmateFactory(DjangoModelFactory):
    class Meta:
        model = Inmate

    first_name = Sequence(lambda n: f"first_name({n})")
    last_name = Sequence(lambda n: f"last_name({n})")
    birth_date = datetime.now() - timedelta(days=365 * 20)
    metadata = LazyFunction(dict)


class PrisonFactory(DjangoModelFactory):
    class Meta:
        model = Prison

    address = Sequence(lambda n: f"Test str., ({n})")
    name = Sequence(lambda n: f"TestPrison({n})")


class ListFactory(DjangoModelFactory):
    class Meta:
        model = List

    date = Sequence(lambda n: datetime.now() - timedelta(days=n))


class ListItemFactory(DjangoModelFactory):
    class Meta:
        model = ListItem

    list = SubFactory(ListFactory)
    first_name = Sequence(lambda n: f"Person.FirstName ({n})")
    last_name = Sequence(lambda n: f"Person.LastName ({n})")
