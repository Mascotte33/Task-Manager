from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/tasksdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    deadline = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        deadline=datetime.strptime(data['deadline'], "%Y-%m-%d")
    )
    db.session.add(task)
    db.session.commit()
    return jsonify({"message": "Task added"}), 201

@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {"id": t.id, "title": t.title, "description": t.description, "deadline": t.deadline.strftime("%Y-%m-%d"), "done": t.done}
        for t in tasks
    ])

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    task.done = True
    db.session.commit()
    return jsonify({"message": "Task marked as done"})

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)