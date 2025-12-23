#!/bin/bash

# Syllabus Accessibility Checker - Web App Startup Script

echo "================================================"
echo "  Syllabus Accessibility Checker - Web App"
echo "================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Flask web server..."
echo "================================================"
echo ""
echo "  🌐 Web app will be available at:"
echo "     http://localhost:5001"
echo ""
echo "  Press Ctrl+C to stop the server"
echo ""
echo "================================================"
echo ""

# Start the Flask app
python app.py
