import json


def test_ping(client):
    resp = client.get('/ping')
    assert resp.status_code == 200
    assert json.loads(resp.data)['ok'] == 'ok'
