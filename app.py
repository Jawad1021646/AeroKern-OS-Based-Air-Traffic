import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.secret_key = 'replace-with-strong-secret'  # needed for flashing messages

# Directory to store uploaded wheels (temporary)
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_wheel():
    if 'wheel' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    file = request.files['wheel']
    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('index'))
    if not file.filename.lower().endswith('.whl'):
        flash('Only .whl files are allowed', 'error')
        return redirect(url_for('index'))
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(save_path)
    # Install the wheel using the virtual environment's pip
    pip_exe = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.venv', 'Scripts', 'pip.exe')
    try:
        result = subprocess.run([pip_exe, 'install', '--upgrade', save_path], capture_output=True, text=True, check=True)
        flash(f'Wheel installed: {file.filename}', 'success')
    except subprocess.CalledProcessError as e:
        flash(f'Installation failed: {e.stderr}', 'error')
    return redirect(url_for('index'))

# Simple static route for any future assets
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    # Run on localhost, default port 5000, enable reloader for development
    app.run(host='127.0.0.1', port=5000, debug=True)
