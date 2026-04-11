from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/test')
def test():
    return "OK"

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/app')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt required'}), 400

    try:
        return jsonify({'result': f"You sent: {prompt}"})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
