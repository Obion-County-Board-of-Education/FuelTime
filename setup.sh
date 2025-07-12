#!/bin/bash

echo "🚀 Fuel Report App Setup & Testing"
echo "=================================="

# Check if docker-compose.yml has been configured
if grep -q "change-this-to-your-app-password" docker-compose.yml; then
    echo ""
    echo "⚠️  SETUP REQUIRED:"
    echo "1. Edit docker-compose.yml"
    echo "2. Replace 'change-this-to-your-app-password' with your actual app password"
    echo "3. Verify SMTP_USERNAME is correct"
    echo ""
    echo "📋 To create an App Password:"
    echo "   - Go to: https://account.microsoft.com/security"
    echo "   - Click 'App passwords'"
    echo "   - Create new password for 'Fuel Report App'"
    echo ""
    read -p "Press Enter when you've updated the configuration..."
fi

echo ""
echo "🔄 Starting application..."
docker-compose down
docker-compose up --build -d

echo ""
echo "⏳ Waiting for application to start..."
sleep 5

echo ""
echo "🧪 Testing email configuration..."
docker-compose exec fuel-report-app python test_email.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "📱 Access the application at: http://localhost:5000"
echo ""
echo "🔍 To view logs: docker-compose logs -f fuel-report-app"
echo "🛑 To stop: docker-compose down"
