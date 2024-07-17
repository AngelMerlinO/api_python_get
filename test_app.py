import pytest
import json
from app import app, DATA_FILE

@pytest.fixture
def client():
    app.config['TESTING'] = True

    # Configurar el entorno de prueba
    with app.test_client() as client:
        yield client

    # Limpiar después de las pruebas
    with open(DATA_FILE, 'w') as f:
        json.dump({'rutines': [], 'exercises': [], 'registers': []}, f)

def test_add_rutine(client):
    response = client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Rutina 1'

def test_get_rutines(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    response = client.get('/rutines')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Rutina 1'

def test_add_exercise(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    response = client.post('/exercise', data=json.dumps({'name': 'Ejercicio 1', 'rutine_id': 1}), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Ejercicio 1'
    assert data['rutine_id'] == 1

def test_get_exercises_by_rutine(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    client.post('/exercise', data=json.dumps({'name': 'Ejercicio 1', 'rutine_id': 1}), content_type='application/json')
    response = client.get('/rutine/1/exercises')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['name'] == 'Ejercicio 1'

def test_add_register(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    client.post('/exercise', data=json.dumps({'name': 'Ejercicio 1', 'rutine_id': 1}), content_type='application/json')
    response = client.post('/register', data=json.dumps({'kilogram': 10.0, 'repetitions': 10, 'series': 3, 'exercise_id': 1}), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['kilogram'] == 10.0
    assert data['repetitions'] == 10
    assert data['series'] == 3
    assert data['exercise_id'] == 1

def test_get_registers_by_exercise(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    client.post('/exercise', data=json.dumps({'name': 'Ejercicio 1', 'rutine_id': 1}), content_type='application/json')
    client.post('/register', data=json.dumps({'kilogram': 10.0, 'repetitions': 10, 'series': 3, 'exercise_id': 1}), content_type='application/json')
    response = client.get('/exercise/1/registers')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 1
    assert data[0]['kilogram'] == 10.0

def test_delete_rutine(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    response = client.delete('/rutine/1')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'Rutine deleted successfully'

def test_update_exercise(client):
    client.post('/rutine', data=json.dumps({'name': 'Rutina 1'}), content_type='application/json')
    client.post('/exercise', data=json.dumps({'name': 'Ejercicio 1', 'rutine_id': 1}), content_type='application/json')
    response = client.put('/exercise/1', data=json.dumps({'name': 'Ejercicio Actualizado'}), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'Ejercicio Actualizado'
