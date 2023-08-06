import unittest.mock as mock
import warnings
from pathlib import Path

import pytest

from acondbs.db.backup import backup_db_to_github


@pytest.fixture()
def mock_backup_db_to_github_(monkeypatch):
    y = mock.Mock()
    monkeypatch.setattr("acondbs.db.backup.backup_db_to_github_", y)
    yield y


@pytest.fixture()
def mock_lock_path(app, monkeypatch, tmpdir_factory):
    folder = Path(tmpdir_factory.mktemp('backup'))
    y = folder.joinpath('lock')
    monkeypatch.setitem(app.config, 'ACONDBS_DB_BACKUP_LOCK', str(y))
    monkeypatch.setitem(app.config, 'ACONDBS_DB_BACKUP_LOCK_TIMEOUT', 0.01)
    yield y


def test_backup_db_to_github(app, mock_lock_path, mock_backup_db_to_github_):
    with app.app_context():
        repo_path = app.config['ACONDBS_DB_FOLDER']
        backup_db_to_github()
    assert [mock.call(repo_path)] == mock_backup_db_to_github_.call_args_list


def test_backup_db_locked(app, mock_lock_path, mock_backup_db_to_github_):
    mock_lock_path.touch()
    with app.app_context():
        with warnings.catch_warnings(record=True) as w:
            backup_db_to_github()
    assert [] == mock_backup_db_to_github_.call_args_list
    assert len(w) == 1
