from flask import Flask, request, jsonify

app = Flask(__name__)

# Almacenamiento en memoria para las tareas
tareas = []

@app.route('/tareas', methods=['GET', 'POST', 'DELETE'])
def manejar_tareas():
    if request.method == 'GET':
        return jsonify(tareas)
    elif request.method == 'POST':
        nueva_tarea = request.json.get('tarea')
        if nueva_tarea:
            tareas.append(nueva_tarea)
            return jsonify({'mensaje': 'Tarea añadida'}), 201
    elif request.method == 'DELETE':
        tarea = request.json.get('tarea')
        if tarea in tareas:
            tareas.remove(tarea)
            return jsonify({'mensaje': 'Tarea eliminada'}), 200
    return jsonify({'mensaje': 'Solicitud inválida'}), 400

if __name__ == '__main__':
    app.run(debug=True)
