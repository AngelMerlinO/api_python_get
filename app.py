from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'data.json'

# Verificar si el archivo JSON existe, si no, crearlo con una estructura vacía
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({'rutines': [], 'exercises': [], 'registers': []}, f)

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

# Endpoint para agregar una nueva rutina
@app.route('/rutine', methods=['POST'])
def add_rutine():
    data = request.get_json()
    rutine = {'id': len(read_data()['rutines']) + 1, 'name': data['name']}
    all_data = read_data()
    all_data['rutines'].append(rutine)
    write_data(all_data)
    return jsonify(rutine)

# Endpoint para obtener todas las rutinas
@app.route('/rutines', methods=['GET'])
def get_rutines():
    return jsonify(read_data()['rutines'])

# Endpoint para agregar un nuevo ejercicio a una rutina
@app.route('/exercise', methods=['POST'])
def add_exercise():
    data = request.get_json()
    exercise = {'id': len(read_data()['exercises']) + 1, 'name': data['name'], 'rutine_id': data['rutine_id']}
    all_data = read_data()
    all_data['exercises'].append(exercise)
    write_data(all_data)
    return jsonify(exercise)

# Endpoint para obtener todos los ejercicios de una rutina específica
@app.route('/rutine/<int:rutine_id>/exercises', methods=['GET'])
def get_exercises_by_rutine(rutine_id):
    exercises = [exercise for exercise in read_data()['exercises'] if exercise['rutine_id'] == rutine_id]
    return jsonify(exercises)

# Endpoint para agregar un nuevo registro a un ejercicio
@app.route('/register', methods=['POST'])
def add_register():
    data = request.get_json()
    register = {
        'id': len(read_data()['registers']) + 1,
        'kilogram': data['kilogram'],
        'repetitions': data['repetitions'],
        'series': data['series'],
        'exercise_id': data['exercise_id']
    }
    all_data = read_data()
    all_data['registers'].append(register)
    write_data(all_data)
    return jsonify(register)

# Endpoint para obtener todos los registros de un ejercicio específico
@app.route('/exercise/<int:exercise_id>/registers', methods=['GET'])
def get_registers_by_exercise(exercise_id):
    registers = [register for register in read_data()['registers'] if register['exercise_id'] == exercise_id]
    return jsonify(registers)

# Endpoint para eliminar una rutina
@app.route('/rutine/<int:rutine_id>', methods=['DELETE'])
def delete_rutine(rutine_id):
    all_data = read_data()
    rutines = all_data['rutines']
    exercises = all_data['exercises']
    registers = all_data['registers']

    rutine = next((rutine for rutine in rutines if rutine['id'] == rutine_id), None)
    if rutine is None:
        return jsonify({'error': 'Rutine not found'}), 404

    exercises_to_delete = [exercise for exercise in exercises if exercise['rutine_id'] == rutine_id]
    for exercise in exercises_to_delete:
        registers = [register for register in registers if register['exercise_id'] != exercise['id']]
        exercises.remove(exercise)

    rutines.remove(rutine)

    all_data['rutines'] = rutines
    all_data['exercises'] = exercises
    all_data['registers'] = registers

    write_data(all_data)
    return jsonify({'message': 'Rutine deleted successfully'})

# Endpoint para actualizar el nombre de un ejercicio
@app.route('/exercise/<int:exercise_id>', methods=['PUT'])
def update_exercise(exercise_id):
    data = request.get_json()
    all_data = read_data()
    exercise = next((exercise for exercise in all_data['exercises'] if exercise['id'] == exercise_id), None)
    if exercise is None:
        return jsonify({'error': 'Exercise not found'}), 404

    exercise['name'] = data['name']
    write_data(all_data)
    return jsonify(exercise)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
