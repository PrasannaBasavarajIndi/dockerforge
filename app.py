import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# Configure SQLite Database
basedir = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(basedir, 'data')
os.makedirs(data_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(data_dir, 'tasks.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title}


with app.app_context():
    db.create_all()

# Global in-memory dictionary for 'build_status' metadata
build_status = {
    'build_number': 'N/A',
    'status': 'Pending',
    'timestamp': 'N/A'
}


@app.route('/')
def index():
    # We no longer pass tasks here, the frontend will fetch them via AJAX
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/api/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted"}), 200
    return jsonify({"error": "Task not found"}), 404


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', build_status=build_status)


@app.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    build_status['build_number'] = data.get('build_number', build_status['build_number'])
    build_status['status'] = data.get('status', build_status['status'])

    ist_time = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    build_status['timestamp'] = ist_time.strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({"message": "Status updated successfully", "current_status": build_status}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
