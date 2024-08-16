import pytest
import time
from flask import Flask
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_ping(client):
    response = client.get('/ping')
    assert response.status_code == 200
    assert response.data == b"Cats Service. Version 0.1"


def test_invalid_attribute(client):
    response = client.get('/cats?attribute=invalid')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid attribute'}


def test_invalid_order(client):
    response = client.get('/cats?order=invalid')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid order'}


def test_get_default_data_cats(client):
    response = client.get('/cats')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) <= 10


def test_add_duplicate_cat(client):
    new_cat = {
        'name': 'Tom',
        'color': 'Gray',
        'tail_length': 30,
        'whiskers_length': 15
    }
    client.post('/cat', json=new_cat)  # добавляем кота
    response = client.post('/cat', json=new_cat)  # пытаемся добавить еще раз
    assert response.status_code == 409
    assert response.get_json() == {'error': 'Cat already exists'}


def test_add_invalid_cat_data(client):
    invalid_data = {
        'name': '',
        'color': 123,  # Invalid color
        'tail_length': -1,  # Invalid tail length
        'whiskers_length': 'long'  # Invalid whiskers length
    }

    response = client.post('/cat', json=invalid_data)
    assert response.status_code == 400
    assert 'Color is invalid' in response.json['error']
    assert 'Tail_length is invalid' in response.json['error']
    assert 'Whiskers_length is invalid' in response.json['error']


def test_rate_limit(client):
    for _ in range(600):
        response = client.get('/cats')
        assert response.status_code == 200, f"Failed at request {_ + 1}"
        time.sleep(0.1)  # Добавляет 100 миллисекунд задержки между запросами

    response = client.get('/cats')
    assert response.status_code == 429, "Expected 429 Too Many Requests"
    assert response.get_json() == {"message": "Rate limit exceeded: 600 per 1 minute"}