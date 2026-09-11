#!/bin/bash

# Setup script for Stock Analysis AI Agent

echo "🚀 Stock Analysis AI Agent - Setup Script"
echo "========================================"

# Check Python version
echo "📝 Checking Python version..."
python --version || python3 --version

# Create virtual environment
echo "📦 Creating Python virtual environment..."
python -m venv venv || python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "📄 Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  Please edit .env file and add your API keys:"
    echo "   - IEX_CLOUD_API_KEY"
    echo "   - ANTHROPIC_API_KEY"
fi

# Initialize database
echo "🗄️  Initializing database..."
alembic upgrade head

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "   1. Edit .env file with your API keys"
echo "   2. Run: uvicorn app.main:app --reload"
echo "   3. Visit: http://localhost:8000/docs"
echo ""
