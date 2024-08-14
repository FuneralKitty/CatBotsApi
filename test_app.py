import pytest
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


def test_get_cats(client, mocker):
    mock_db_response = [
        ('Tihon', 'red & white', 15, 12),
        ('Murzik', 'gray', 10, 8)
    ]

    mocker.patch('app.psycopg.connect').return_value.cursor(
    ).fetchall.return_value = mock_db_response

    response = client.get('/cats')
    assert response.status_code == 200
    assert response.json == [{'name': 'Tihon',
                              'color': 'red & white',
                              'tail_length': 15,
                              'whiskers_length': 12},
                             {'name': 'Murzik',
                              'color': 'gray',
                              'tail_length': 10,
                              'whiskers_length': 8}]


def test_add_valid_cat(client, mocker):
    mock_db_connect = mocker.patch('app.psycopg.connect')
    mock_cursor = mock_db_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = None  # Cat does not exist

    data = {
        'name': 'Tihon',
        'color': 'red & white',
        'tail_length': 15,
        'whiskers_length': 12
    }

    response = client.post('/cat', json=data)
    assert response.status_code == 201
    assert response.json == {'message': 'Cat added successfully'}


def test_add_duplicate_cat(client, mocker):
    mock_db_connect = mocker.patch('app.psycopg.connect')
    mock_cursor = mock_db_connect.return_value.cursor.return_value
    mock_cursor.fetchone.return_value = ('Tihon',)  # Cat already exists

    data = {
        'name': 'Tihon',
        'color': 'red & white',
        'tail_length': 15,
        'whiskers_length': 12
    }

    response = client.post('/cat', json=data)
    assert response.status_code == 409
    assert response.json == {'error': 'Cat already exists'}


def test_add_invalid_cat_data(client):
    invalid_data = {
        'name': 'Tihon',
        'color': 123,  # Invalid color
        'tail_length': -1,  # Invalid tail length
        'whiskers_length': 'long'  # Invalid whiskers length
    }

    response = client.post('/cat', json=invalid_data)
    assert response.status_code == 400
    assert 'Color is invalid' in response.json['error']
    assert 'Tail_length is invalid' in response.json['error']
    assert 'Whiskers_length is invalid' in response.json['error']
