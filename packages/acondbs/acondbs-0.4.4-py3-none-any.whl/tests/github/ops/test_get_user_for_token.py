import pytest
import sqlalchemy

from acondbs.github import ops


def test_success(app, snapshot):
    token = 'token3'
    with app.app_context():
        user = ops.get_user_for_token(token)
    assert 'user2' == user.login


def test_error(app, snapshot):
    token = 'no-such-token'
    with app.app_context():
        with pytest.raises(sqlalchemy.orm.exc.NoResultFound):
            _ = ops.get_user_for_token(token)
