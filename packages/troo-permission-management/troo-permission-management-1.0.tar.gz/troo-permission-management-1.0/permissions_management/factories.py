import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from factory import Faker, post_generation
from factory.django import DjangoModelFactory


class UserFactory(DjangoModelFactory):
    email = Faker("email")
    username = email
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    is_active = True
    is_superuser = False

    @post_generation
    def password(self, create: bool, extracted, **kwargs):
        password = (
            extracted
            if extracted
            else Faker(
                "password",
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            ).evaluate(None, None, extra={"locale": None})
        )
        self.set_password(password)

    class Meta:
        model = get_user_model()
        django_get_or_create = ["email"]


class GroupFactory(DjangoModelFactory):
    name = factory.Sequence(lambda n: "group - %d" % n)

    class Meta:
        model = Group
        django_get_or_create = ["name"]
