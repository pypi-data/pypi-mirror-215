import pytest
from a2wsgi import WSGIMiddleware
from async_asgi_testclient import TestClient

import acondbs

QUERY = "{ version }"


@pytest.mark.asyncio
async def test_schema(app):
    app = WSGIMiddleware(app)  # convert a wsgi app to an asgi app

    headers = {
        "Content-Type:": "application/json",
        "Authorization": "Bearer token123",  # octocat
    }

    data = {"query": QUERY}
    expected = {"data": {"version": acondbs.__version__}}

    async with TestClient(app) as client:
        resp = await client.post("/graphql", json=data, headers=headers)

    assert resp.status_code == 200
    assert resp.json() == expected
