---
title: Afiya Care Backend
emoji: 🏥
colorFrom: blue
colorTo: green
sdk: docker
pinned: false
license: mit
---

# Afiya Care - AI Health Assistant

Powered by N-ATLaS (NCAIR1/N-ATLaS)

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /api/v1/diagnose` - Symptom diagnosis
- `GET /api/v1/languages` - Supported languages
- `GET /docs` - Interactive API documentation

## Supported Languages
- English
- Yoruba
- Hausa
- Igbo
- Nigerian Pidgin

## Usage
```bash
curl -X POST "https://YOUR_USERNAME-afiya-care-backend.hf.space/api/v1/diagnose" \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a headache", "language": "en"}'
```
Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
