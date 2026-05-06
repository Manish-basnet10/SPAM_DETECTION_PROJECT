#!/bin/bash
# =============================================
# SpamGuard - Start All Services
# =============================================
echo "🚀 Starting SpamGuard..."
echo ""

# Kill any existing processes on ports 5001 and 3000
echo "🔄 Clearing ports..."
lsof -ti :5001 | xargs kill -9 2>/dev/null
lsof -ti :3000 | xargs kill -9 2>/dev/null
sleep 1

# Start MongoDB (if not running)
echo "🗄️  Ensuring MongoDB is running..."
brew services start mongodb-community@7.0 2>/dev/null || true
sleep 2

# Start Flask backend
echo "⚙️  Starting Flask backend on port 5000..."
cd "$(dirname "$0")/spam-backend"
python3 app.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"
sleep 3

# Verify backend
if curl -s http://127.0.0.1:5001/health > /dev/null 2>&1; then
  echo "   ✅ Backend is healthy"
else
  echo "   ❌ Backend failed to start — check spam-backend/app.py"
fi

# Start React frontend
echo "🌐 Starting React frontend on port 3000..."
cd "$(dirname "$0")/spam-frontend"
npm start &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "============================================"
echo "✅ SpamGuard is starting up!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:5001  (NOTE: port 5000 is macOS AirPlay)"
echo "   MongoDB:  mongodb://localhost:27017"
echo "============================================"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both
wait $BACKEND_PID $FRONTEND_PID
