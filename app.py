import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from models import db, Settings, PromoJob
from services.encryption import EncryptionService
from celery import Celery
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///promo_kit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev_key')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

db.init_app(app)

# Celery Configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='redis://localhost:6379/0',
        broker='redis://localhost:6379/0'
    )
    celery.conf.update(app.config)
    return celery

celery = make_celery(app)

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
    
    # Placeholder for actual API test logic
    # In production, this would call OpenAI/Gemini
    return jsonify({"success": True, "message": f"API key test successful for {provider} ({model})"})

@app.route('/save-settings', methods=['POST'])
def save_settings():
    data = request.json
    provider = data.get('provider')
    model = data.get('model')
    api_key = data.get('api_key')
    
    try:
        encryptor = EncryptionService()
        encrypted_key = encryptor.encrypt(api_key)
        
        # Keep only latest row
        db.session.query(Settings).delete()
        new_settings = Settings(provider=provider, model=model, api_key=encrypted_key)
        db.session.add(new_settings)
        db.session.commit()
        return jsonify({"success": True, "message": "Settings saved successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@app.route('/generate', methods=['POST'])
def generate():
    # Start background job
    job_id = str(uuid.uuid4())
    # trigger celery task here
    return jsonify({"task_id": job_id})

@app.route('/status/<task_id>')
def status(task_id):
    # Check status from DB or Celery
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
    app.run(host='0.0.0.0', port=5000)
