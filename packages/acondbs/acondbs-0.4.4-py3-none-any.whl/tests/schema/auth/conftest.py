import pytest


@pytest.fixture
def app(app_users):
    y = app_users
    yield y
