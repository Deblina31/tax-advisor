# Frontend Testing Guide: Gemini Flash 2.0 Pro Integration

## 🚀 Quick Start

### 1. Set Up Your Gemini API Key
First, you need to get a Gemini API key and configure it:

1. **Get API Key:**
   - Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Sign in with your Google account
   - Create a new API key
   - Copy the API key

2. **Configure Environment:**
   ```bash
   # Copy the environment template
   cp environment_sample.txt .env
   
   # Edit .env file and add your API key
   GEMINI_API_KEY=your-actual-api-key-here
   ```

### 2. Start the Application
```bash
# Activate virtual environment (if using)
cd tax-advisor
source bin/activate  # On Windows: Scripts\activate

# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the application
python main.py
```

The application will start at: `http://localhost:8000`

## 🎯 Testing the AI Integration

### Option 1: Interactive Web Demo
1. **Open the AI Demo Page:**
   - Navigate to: `http://localhost:8000/ai-demo`
   - Or click the "AI Demo" link in the navigation bar

2. **Test Different Features:**
   - **Service Status**: Check if AI service is running
   - **Connection Test**: Verify API connectivity
   - **Tax Suggestions**: Generate personalized tax advice
   - **Regime Comparison**: Compare old vs new tax regimes
   - **AI Chat**: Interactive conversation with AI

### Option 2: API Testing with curl
```bash
# 1. Check service status
curl -X GET "http://localhost:8000/api/ai/status"

# 2. Test connection
curl -X POST "http://localhost:8000/api/ai/test-connection"

# 3. Generate tax suggestions
curl -X POST "http://localhost:8000/api/ai/tax-suggestions" \
  -H "Content-Type: application/json" \
  -d '{
    "basic_salary": 600000,
    "hra": 240000,
    "other_allowances": 60000,
    "gross_salary": 900000,
    "current_deductions": 50000,
    "net_salary": 700000,
    "age": 30,
    "marital_status": "Single",
    "dependents": 0,
    "city": "Mumbai",
    "rent_paid": 25000,
    "current_investments": "PPF: ₹50,000, ELSS: ₹30,000",
    "financial_goals": "Home purchase in 5 years, Retirement planning",
    "session_id": "test_123"
  }'

# 4. Compare tax regimes
curl -X POST "http://localhost:8000/api/ai/regime-comparison" \
  -H "Content-Type: application/json" \
  -d '{
    "gross_salary": 900000,
    "basic_salary": 600000,
    "hra": 240000,
    "other_allowances": 60000,
    "section_80c": 80000,
    "section_80d": 15000,
    "home_loan_interest": 0,
    "other_deductions": 0,
    "age": 30,
    "city": "Mumbai",
    "rent_paid": 25000,
    "session_id": "test_123"
  }'

# 5. Chat with AI
curl -X POST "http://localhost:8000/api/ai/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_query": "How can I save more tax with my current income of ₹9 lakhs?",
    "session_id": "test_123",
    "user_profile": "Software Engineer, Age 30"
  }'
```

### Option 3: Python Script Testing
```bash
# Run the comprehensive test suite
python test_gemini_integration.py
```

## 🔍 What to Expect

### 1. Service Status Response
```json
{
  "is_available": true,
  "model_name": "gemini-2.0-flash-exp",
  "rate_limits": {
    "requests_per_minute": 60,
    "requests_per_hour": 1000,
    "current_minute_requests": 0,
    "current_hour_requests": 0
  },
  "configuration": {
    "max_tokens": 8192,
    "temperature": 0.7,
    "max_retries": 3,
    "retry_delay": 1
  }
}
```

### 2. Tax Suggestions Response
```json
{
  "success": true,
  "response_type": "tax_suggestions",
  "content": "## Tax Analysis Summary\nBased on your income of ₹9,00,000...",
  "confidence_score": 0.85,
  "processing_time": 2.34,
  "tokens_used": 1250,
  "suggestions": [
    {
      "title": "ELSS Mutual Funds",
      "description": "Invest ₹50,000 for potential savings of ₹15,000",
      "category": "investment",
      "priority": "high",
      "potential_savings": 15000
    }
  ],
  "action_items": [
    "Complete Section 80C investments by March",
    "Consider increasing health insurance coverage"
  ],
  "disclaimers": [
    "This advice is for informational purposes only..."
  ]
}
```

### 3. Chat Response
```json
{
  "success": true,
  "response_type": "chat_response",
  "content": "Based on your income of ₹9 lakhs, here are several ways to save tax:\n\n1. **Section 80C Investments** - You can invest up to ₹1.5 lakh...",
  "confidence_score": 0.92,
  "processing_time": 1.87,
  "tokens_used": 890,
  "disclaimers": [
    "This advice is for informational purposes only..."
  ]
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **"AI service is not available"**
   - Check if `GEMINI_API_KEY` is set in your `.env` file
   - Verify the API key is valid
   - Check internet connectivity

2. **"Rate limit exceeded"**
   - Wait for the rate limit to reset
   - Check current usage in service status

3. **"Failed to generate AI response"**
   - Check API key permissions
   - Verify Gemini API is accessible from your location
   - Check application logs for detailed error messages

4. **Frontend not loading**
   - Ensure the application is running on port 8000
   - Check browser console for JavaScript errors
   - Verify all static files are accessible

### Debug Steps

1. **Check Service Status:**
   ```bash
   curl -X GET "http://localhost:8000/api/ai/status"
   ```

2. **Test Basic Connection:**
   ```bash
   curl -X POST "http://localhost:8000/api/ai/test-connection"
   ```

3. **Check Application Logs:**
   - Look for error messages in the terminal where you started the application
   - Check for import errors or configuration issues

4. **Verify Environment:**
   ```bash
   # Check if environment variables are loaded
   python -c "from config.settings import settings; print(f'API Key configured: {bool(settings.GEMINI_API_KEY)}')"
   ```

## 📊 Performance Monitoring

The demo interface shows real-time metrics:
- **Response Time**: How long the AI takes to respond
- **Tokens Used**: Number of tokens consumed
- **Confidence Score**: AI's confidence in the response
- **Success Rate**: Whether requests are successful

## 🎨 Frontend Features

### Interactive Demo Page
- **Real-time Status**: Live service status monitoring
- **Form Validation**: Input validation for all fields
- **Response Formatting**: Beautiful display of AI responses
- **Error Handling**: User-friendly error messages
- **Performance Metrics**: Real-time performance monitoring

### Navigation
- **Main App**: Original PDF upload functionality at `/`
- **AI Demo**: New AI testing interface at `/ai-demo`
- **API Docs**: FastAPI auto-generated docs at `/docs`

## 🔗 API Endpoints Summary

| Endpoint | Method | Purpose |
|----------|---------|---------|
| `/api/ai/status` | GET | Check service status |
| `/api/ai/test-connection` | POST | Test API connectivity |
| `/api/ai/tax-suggestions` | POST | Generate tax suggestions |
| `/api/ai/regime-comparison` | POST | Compare tax regimes |
| `/api/ai/chat` | POST | Chat with AI advisor |
| `/api/ai/health` | GET | Health check |

## 🚀 Next Steps

1. **Test with Real Data**: Use your actual salary information
2. **Explore Different Scenarios**: Try various income levels and situations
3. **Frontend Integration**: Integrate AI features into the main PDF upload flow
4. **User Experience**: Enhance the UI based on user feedback
5. **Performance Optimization**: Monitor and optimize based on usage patterns

## 📝 Notes

- The AI responses are generated in real-time and may take 2-4 seconds
- All data is processed securely and not stored permanently
- The demo uses sample data that you can modify
- Rate limits are in place to prevent API abuse
- All responses include disclaimers about the advisory nature of the content

Happy testing! 🎉 