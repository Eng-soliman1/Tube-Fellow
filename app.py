from flask import Flask, render_template, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

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
    api_key = data.get('api_key')
    
    if not api_key:
        return jsonify({'error': 'API Key مطلوب'}), 400
    if not prompt:
        return jsonify({'error': 'Prompt مطلوب'}), 400
    
    try:
        client = Open(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert YouTube Growth Hacker with 10+ years of experience.
                    You specialize in:
                    - High-retention video patterns (Hooks, Loops, Pacing)
                    - High-CPM niches (Finance, SaaS, Tech)
                    - Viral Psychology (CTR optimization and Audience Retention)
                    - Script writing that keeps viewers watching till the end
                    Always respond in professional English."""
                },
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content
        return jsonify({'result': result})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
