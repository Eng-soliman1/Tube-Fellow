from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)


@app.route('/')
def landing():
    return "WORKING"


@app.route('/app')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    prompt = data.get('prompt')
    api_key = data.get('api_key')

    if not api_key:
        return jsonify({'error': 'API Key مطلوب'}), 400
    if not prompt:
        return jsonify({'error': 'Prompt مطلوب'}), 400

    try:
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert YouTube Growth Hacker..."
                },
                {"role": "user", "content": prompt}
            ]
        )

        result = response.choices[0].message.content
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
        return jsonify({'error': str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
