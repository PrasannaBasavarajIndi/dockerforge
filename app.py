from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime, timedelta, timezone

app = Flask(__name__)

# Global in-memory storage for tasks
tasks = []
task_id_counter = 1

# Global in-memory dictionary for 'build_status' metadata
build_status = {
    'build_number': 'N/A',
    'status': 'Pending',
    'timestamp': 'N/A'
}

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    global task_id_counter
    title = request.form.get('title')
    if title:
        tasks.append({'id': task_id_counter, 'title': title})
        task_id_counter += 1
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return redirect(url_for('index'))

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
    
    # Calculate IST correctly since Docker containers run in UTC by default
    ist_time = datetime.now(timezone.utc) + timedelta(hours=5, minutes=30)
    build_status['timestamp'] = ist_time.strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({"message": "Status updated successfully", "current_status": build_status}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
