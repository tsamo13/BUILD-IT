import pytest
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"<html" in response.data  # απλά δείχνει ότι φορτώνει HTML

@patch('app.get_db_connection')
def test_search_form(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [('Electrical',), ('Plumbing',)]
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.get('/search_form')
    assert response.status_code == 200
    assert b'Plumbing' in response.data or b'Electrical' in response.data

@patch('app.get_db_connection')
def test_search_results(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [
        (1, 'Workshop A', 'Some description', 'Athens')
    ]
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.post('/search', data={
        'location': 'Athens',
        'type': 'Electrical'
    })
    assert response.status_code == 200
    assert b'Workshop A' in response.data

@patch('app.get_db_connection')
def test_choose_workshop(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ('Fixing stuff', 'Electrical', 'Athens', 'Workshop A')
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.post('/choose', data={'workshop_id': '1'})
    assert response.status_code == 200
    assert b'Workshop A' in response.data

@patch('app.get_db_connection')
def test_apply(mock_get_conn, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    mock_get_conn.return_value = mock_conn

    response = client.post('/apply', data={
        'name': 'Company A',
        'construction_id': '10',
        'email': 'company@example.com',
        'project_title': 'Bridge Construction'
    })

    assert response.status_code == 200
    assert b'Bridge Construction' in response.data
