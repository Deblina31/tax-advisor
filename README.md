# 🧾 AI Tax Advisor Demo

A standalone demo app built during my **Summer Internship at Setu (Pine Labs Group)** that showcases the use of **Generative AI** to provide personalized Indian tax advisory for FY 2024–25.

## 🔍 Overview

The AI Tax Advisor Demo integrates **Google's Gemini Flash 2.0 Pro** to assist users with:
- 💡 **Tax-saving suggestions** based on salary inputs
- ⚖️ **Old vs New regime comparisons** with detailed analysis
- 💬 **Interactive AI chat** for tax-related questions
- 📊 **Real-time metrics** including response time, confidence score & token usage
- ✅ **Service health monitoring** for backend/AI status

> ⚠️ This tool is for **demo/testing** purposes only and not a substitute for certified tax advice.

---

## ⚙️ Tech Stack

- **Backend**: FastAPI (Python)
- **LLM Integration**: Google Gemini Flash 2.0 Pro
- **Frontend**: HTML-based interactive demo (`ai_demo.html`)
- **API Design**: RESTful endpoints for:
  - Tax Suggestions
  - Regime Comparison
  - AI Chat
  - Health Check

---

## 🚀 Features Implemented

- 🧠 Prompt-engineered responses from Gemini AI tailored for Indian tax scenarios
- 🔗 RESTful API with modular endpoints
- 📈 Real-time performance tracking (latency, tokens, model confidence)
- 🧪 Designed for extensibility and future deployment
- 🌐 Clean, minimal web-based interface for user testing

---

## 🛠️ Setup Instructions

```bash
# Clone the repository
git clone https://github.com/your-username/ai-tax-advisor.git
cd ai-tax-advisor

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --reload
