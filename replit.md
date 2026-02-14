# PromoKit - Book Promo Generator

## Overview
A Flask web application for generating promotional kits for books. Users can input book details (title, subtitle, author, genre, description, target audience, price) and generate promo materials. Includes settings page for configuring AI provider API keys (OpenAI/Gemini).

## Current State
- MVP with form-based UI for book promo generation
- Settings page for AI provider configuration with encrypted API key storage
- SQLite database for settings and job tracking
- Dark-themed UI

## Project Architecture
- **Framework**: Flask (Python 3.11)
- **Database**: SQLite (local file `instance/promo_kit.db`)
- **Server**: Gunicorn on port 5000
- **Key Files**:
  - `app.py` - Main Flask application with routes
  - `main.py` - Entry point (imports app)
  - `models.py` - SQLAlchemy models (Settings, PromoJob)
  - `services/encryption.py` - Fernet encryption for API keys
  - `templates/` - Jinja2 templates (base, index, settings)
  - `static/` - Static assets, manifest, service worker

## Recent Changes
- 2026-02-14: Migrated to Replit environment, installed dependencies, configured workflow

## User Preferences
- None recorded yet
