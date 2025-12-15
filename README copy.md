# Afiya Care Backend - N-ATLaS Powered Medical Assistant

AI-powered medical assistance with N-ATLaS multilingual support for Awarri Hackathon.

## Features
- 🇳🇬 N-ATLaS integration (Yoruba, Hausa, Igbo, Pidgin, English)
- 🔍 Vector-based medical knowledge search
- ⚠️ Red flag detection for emergencies
- 🔒 JWT authentication
- 📱 Offline sync support
- 🐳 Docker deployment ready

## Quick Start
```bash
# Setup
chmod +x setup.sh
./setup.sh

# Start
docker-compose up -d

# API Docs
open http://localhost:8000/docs
```

## Test
```bash
curl -X POST "http://localhost:8000/api/v1/diagnose" \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "Mo ni irora ori", "language": "yo"}'
```

## Model
- **N-ATLaS**: NCAIR1/N-ATLaS (Llama-3 8B)
- **Embeddings**: paraphrase-multilingual-MiniLM-L12-v2

## License
MIT