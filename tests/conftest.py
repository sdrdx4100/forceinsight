import pytest
from django.contrib.auth import get_user_model

from catalog.models import Vehicle


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username='tester', password='pass', role='analyst')


@pytest.fixture
def vehicle(db):
    return Vehicle.objects.create(model_code='TEST-CAR', year=2024)
