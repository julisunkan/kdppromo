import os
import logging

from flask import Flask, render_template, request, jsonify, send_from_directory
from models import db, Settings, PromoJob
from services.encryption import EncryptionService
import uuid

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///promo_kit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    current_settings = Settings.query.order_by(Settings.created_at.desc()).first()
    return render_template('settings.html', settings=current_settings)

@app.route('/test-api', methods=['POST'])
def test_api():
    data = request.json
    provider = data.get('provider')
    model = data.get('model')
    api_key = data.get('api_key')

    if not api_key:
        return jsonify({"success": False, "message": "API key is required"})

    try:
        if provider == 'openai':
            import openai
            client = openai.OpenAI(api_key=api_key)
            # Minimal call to verify key
            client.models.list()
        elif provider == 'gemini':
            import google.generativeai as genai
            genai.configure(api_key=api_key)
            # Minimal call to verify key
            genai.list_models()
        else:
            return jsonify({"success": False, "message": "Invalid provider"})

        return jsonify({"success": True, "message": f"API key test successful for {provider} ({model})"})
    except Exception as e:
        logging.error(f"API validation error: {str(e)}")
        return jsonify({"success": False, "message": f"API key validation failed: {str(e)}"})

@app.route('/save-settings', methods=['POST'])
def save_settings():
    data = request.json
    provider = data.get('provider')
    model = data.get('model')
    api_key = data.get('api_key')

    try:
        encryptor = EncryptionService()
        encrypted_key = encryptor.encrypt(api_key)

        db.session.query(Settings).delete()
        new_settings = Settings(provider=provider, model=model, api_key=encrypted_key)
        db.session.add(new_settings)
        db.session.commit()
        return jsonify({"success": True, "message": "Settings saved successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    job_id = str(uuid.uuid4())
    return jsonify({"task_id": job_id})

@app.route('/status/<task_id>')
def status(task_id):
    return jsonify({"status": "completed", "tokens": 1200, "cost": 0.05, "download_url": "/download/test.zip"})

@app.route('/service-worker.js')
def sw():
    return send_from_directory('static', 'service-worker.js', mimetype='application/javascript')

@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json', mimetype='application/json')

@app.route('/download/<filename>')
def download_zip(filename):
    return send_from_directory('static/zips', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
