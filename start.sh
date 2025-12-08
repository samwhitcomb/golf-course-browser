#!/bin/bash

# Start script for Golf Course Image Scraper

echo "Starting Golf Course Image Scraper..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

# Check if virtual environment exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies if needed
if [ ! -f "venv/.installed" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Install Node dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Start Flask backend in background (uses PORT env, default 5001)
export PORT=${PORT:-5001}
echo "Starting Flask backend on port $PORT..."
python3 app.py &
FLASK_PID=$!

# Wait a moment for Flask to start
sleep 2

# Start Vite frontend
echo "Starting React frontend on port 3000..."
echo ""
echo "Application will be available at http://localhost:3000"
echo "Press Ctrl+C to stop both servers"
echo ""

npm run dev

# Cleanup: kill Flask when script exits
trap "kill $FLASK_PID 2>/dev/null" EXIT

