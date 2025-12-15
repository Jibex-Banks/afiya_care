# #!/bin/bash
# echo "🚀 Afiya Care Setup"
# echo "==================="

# # Create directories
# mkdir -p models alembic/versions

# # Copy .env
# if [ ! -f .env ]; then
#     cp .env.example .env
#     echo "✅ Created .env file"
# fi

# # Start Docker services
# echo "🐳 Starting services..."
# docker-compose up -d postgres qdrant redis
# sleep 10

# # Install dependencies
# echo "📦 Installing dependencies..."
# pip install -r requirements.txt

# # Run migrations
# echo "🗄️ Running migrations..."
# alembic upgrade head

# echo "✅ Setup complete!"
# echo "Start backend: uvicorn app.main:app --reload"


# CMD

@echo off
echo 🚀 Afiya Care Setup
echo ===================

REM --- Create directories ---
if not exist models mkdir models
if not exist alembic mkdir alembic
if not exist alembic\versions mkdir alembic\versions

REM --- Copy .env if missing ---
if not exist .env (
    copy .env.example .env
    echo ✅ Created .env file
)

REM --- Start Docker services ---
echo 🐳 Starting services...
docker-compose up -d postgres qdrant redis
timeout /t 10 >nul

REM --- Install dependencies ---
echo 📦 Installing dependencies...
pip install -r requirements.txt

REM --- Run migrations ---
echo 🗄️ Running migrations...
alembic upgrade head

echo ✅ Setup complete!
echo Start backend: uvicorn app.main:app --reload
pause
