# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, jsonify
import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
# pyrefly: ignore [missing-import]
import password_manager

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/validate', methods=['POST'])
def validate():
    data = request.json
    password = data.get('password', '')
    result = password_manager.validate_password(password)
    return jsonify(result)

@app.route('/api/generate_words', methods=['POST'])
def generate_words():
    data = request.json
    words = data.get('words', '')
    password = password_manager.generate_from_words(words)
    return jsonify({'password': password})

@app.route('/api/generate_random', methods=['GET'])
def generate_random():
    password = password_manager.generate_random()
    return jsonify({'password': password})

@app.route('/api/generate_multiple', methods=['POST'])
def generate_multiple():
    data = request.json
    words = data.get('words', '')
    passwords = password_manager.generate_multiple_from_words(words)
    return jsonify({'passwords': passwords})

@app.route('/api/validate_detailed', methods=['POST'])
def validate_detailed():
    data = request.json
    password = data.get('password', '')
    result = password_manager.validate_password_detailed(password)
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

