#!/bin/bash
# Fast API Banking Chatbot - Startup Script

echo "🏦 Banking Chatbot FastAPI Server"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

# Check if we're in the backend directory
if [ ! -f "main.py" ]; then
    echo "❌ main.py not found. Please run this script from the backend directory."
    exit 1
fi

# Install/update requirements
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "✅ Dependencies installed!"
echo ""
echo "🚀 Starting FastAPI server..."
echo "API available at: http://localhost:8000"
echo "Docs available at: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run the server
python main.py
