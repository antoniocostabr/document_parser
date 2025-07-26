#!/bin/bash

# Document Parser Startup Script

echo "🚀 Starting Document Parser Platform"
echo "======================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from example..."
    cp .env.example .env
    echo "📝 Please edit .env file and add your OpenAI API key before starting the server."
    echo "   Required: OPENAI_API_KEY=your_key_here"
    exit 1
fi

# Check if OpenAI API key is set
if grep -q "your_openai_api_key_here" .env; then
    echo "⚠️  Please set your OpenAI API key in the .env file before starting the server."
    echo "   Edit .env and replace 'your_openai_api_key_here' with your actual API key."
    exit 1
fi

echo "✅ Setup complete!"
echo ""
echo "🌐 Starting server..."
python app.py
