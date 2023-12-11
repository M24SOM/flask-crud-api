from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'

db = SQLAlchemy(app)

'''
CREATE TABLE IF NOT EXISTS todo (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(100)
);
'''


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100))

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


# create the database and tables
with app.app_context():
    db.create_all()


# Routes

@app.route('/', methods=['GET'])
def hello_world():
    return {"message": "Hello Flask"}


# Create an Todo

"""
INSERT INTO todo (name, description) VALUES (%s, %s)
"""


@app.route('/add', methods=['POST'])
def create_todo():
    data = request.get_json()
    new_todo = Todo(name=data['name'], description=data['description'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({"message": "Todo created successfully"}), 201


# Get all Todos

"""
SELECT id, name, description FROM todo
"""


@app.route('/all', methods=['GET'])
def get_all_todos():
    todos = Todo.query.all()
    results = []
    for todo in todos:
        results.append(todo.json())
    return jsonify({'todos': results})


# Get a specific Todo

"""
SELECT id, name, description FROM todo WHERE id = %s
"""


@app.route('/todo/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        return jsonify(todo.json()), 200
    else:
        return jsonify({
            "message": "NOT FOUND"
        }), 404


# Update an Todo

"""
UPDATE todo SET name = %s, description = %s WHERE id = %s
"""


@app.route('/todo/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.name = data['name']
    todo.description = data['description']
    db.session.commit()
    return jsonify({
        'message': 'Todo updated successfully'
    })


# Delete an Todo


"""
DELETE FROM todo WHERE id = %s
"""


@app.route('/todo/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({
        'message': 'Todo deleted successfully'
    })


if __name__ == '__main__':
    app.run(debug=True)
