import pytest


@pytest.fixture
def app(app_empty):
    y = app_empty
    yield y
