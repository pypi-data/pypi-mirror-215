import unittest.mock as mock

import pytest

from acondbs.db.backup import request_backup_db, run_flask_backup_db


@pytest.fixture()
def mock_cap_exec_rate(monkeypatch):
    y = mock.Mock()
    monkeypatch.setattr("acondbs.db.backup.cap_exec_rate", y)
    yield y


def test_request_backup_db(app, mock_cap_exec_rate):
    with app.app_context():
        pause = app.config['ACONDBS_DB_BACKUP_PAUSE']

    nrequests = 3
    with app.app_context():
        for i in range(nrequests):
            request_backup_db()

    assert 1 == mock_cap_exec_rate.call_count
    assert [
        mock.call(func=run_flask_backup_db, pause_time=pause, daemon=True)
    ] == mock_cap_exec_rate.call_args_list

    assert nrequests == mock_cap_exec_rate().call_count
