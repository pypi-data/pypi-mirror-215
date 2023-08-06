from acondbs.github.ops import get_github_oauth_app_info


def test_call(app, snapshot):
    with app.app_context():
        snapshot.assert_match(get_github_oauth_app_info())
