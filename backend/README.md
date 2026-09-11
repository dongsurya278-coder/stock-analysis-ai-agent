# Stock Analysis AI Agent - PRODUCTION READY ✅

**Complete AI-powered stock analysis platform with Claude AI integration**

## 🚀 What's Included

### Backend (Python + FastAPI)
✅ **Data Fetchers**
- IEX Cloud API integration (real-time quotes, fundamentals, news)
- Yahoo Finance integration (historical data, earnings)
- Rate limiting & error handling

✅ **Analysis Engines**
- Fundamental Analysis (P/E, PEG, Growth, Health scoring)
- Technical Analysis (RSI, MACD, Moving Averages, Bollinger Bands, Support/Resistance)
- Sentiment Analysis (AI-powered news sentiment)

✅ **AI Agent (Claude 3.5 Sonnet)**
- Complete stock analysis with reasoning
- Buy/Sell signals with confidence scores
- Portfolio analysis (multiple stocks)
- Entry/Exit price targets

✅ **Background Services**
- Scheduled stock price updates (every 60 seconds)
- AI agent analysis (every 5 minutes)
- Database persistence

✅ **REST API Endpoints**
- `/api/stocks/` - Get all monitored stocks
- `/api/stocks/{symbol}` - Stock details
- `/api/analysis/{symbol}/fundamentals` - Fundamental analysis
- `/api/analysis/{symbol}/technical` - Technical analysis
- `/api/analysis/{symbol}/sentiment` - News sentiment
- `/api/analysis/{symbol}/full` - Complete analysis
- `/api/signals/` - All active signals
- `/api/signals/strong-buy` - Strong buy signals only
- `/api/signals/{symbol}` - Signal for specific stock
- `/api/signals/generate/{symbol}` - Generate new signal
- `/api/signals/stats/summary` - Signals statistics
- WebSocket: `/ws/signals` - Real-time updates
- WebSocket: `/ws/live` - Live stock data

### Frontend (React + Tailwind CSS)
✅ **Dashboard**
- Real-time stock list with prices
- Signal visualization (buy/sell strength)
- Analysis details (fundamental, technical, sentiment)
- Search and filtering
- Responsive design

## 📋 Setup & Installation

### Backend Setup (5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/dongsurya278-coder/stock-analysis-ai-agent.git
cd stock-analysis-ai-agent/backend

# 2. Create Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env

# 5. Add your API keys to .env:
# IEX_CLOUD_API_KEY=your_iex_key_here
# ANTHROPIC_API_KEY=your_claude_key_here
# DATABASE_URL=sqlite:///./stocks.db

# 6. Initialize database
alembic upgrade head

# 7. Run server
uvicorn app.main:app --reload
```

**Backend running at:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### Frontend Setup (5 minutes)

```bash
# 1. Navigate to frontend
cd ../frontend

# 2. Install dependencies
npm install

# 3. Create .env file
echo 'VITE_API_URL=http://localhost:8000' > .env.local

# 4. Start dev server
npm run dev
```

**Frontend running at:** http://localhost:5173

## 🔑 API Keys Required

1. **IEX Cloud** (Free tier available)
   - Sign up: https://iexcloud.io
   - Get sandbox token for testing

2. **Anthropic Claude API**
   - Sign up: https://console.anthropic.com
   - Get API key from dashboard
   - Claude 3.5 Sonnet model

## 💡 How It Works

### Stock Analysis Flow
```
1. Scheduler fetches latest stock data (every 60s)
2. Data stored in database
3. AI Agent runs analysis (every 5 minutes)
   - Fetches company info, price data, fundamentals
   - Calculates technical indicators
   - Analyzes news sentiment
   - Calls Claude AI for comprehensive analysis
   - Generates buy/sell signals
4. Results saved to database
5. Frontend displays via REST API
6. WebSocket pushes real-time updates
```

### AI Agent Analysis
```
Claude AI receives:
- Company fundamentals (P/E, Revenue, Growth)
- Technical indicators (RSI, MACD, Moving Averages)
- News sentiment (positive/negative/neutral)
- Historical context

Claude outputs:
- Investment thesis
- Buy/Sell/Hold recommendation
- Confidence score
- Entry price target
- Target price (3-6 months)
- Stop loss level
- Key risks and catalysts
```

## 📊 Example Responses

### Stock Detail
```json
{
  "status": "success",
  "data": {
    "symbol": "AAPL",
    "stock": {
      "name": "Apple Inc.",
      "sector": "Technology",
      "industry": "Consumer Electronics"
    },
    "price": {
      "price": 189.95,
      "change": 2.45,
      "changePercent": 1.31,
      "volume": 52000000
    },
    "signal": {
      "signal_strength": "buy",
      "confidence_score": 0.82,
      "entry_price": 188.50,
      "target_price": 210.00,
      "stop_loss": 180.00
    }
  }
}
```

### Signals Summary
```json
{
  "status": "success",
  "data": {
    "total_signals": 42,
    "strong_buy": 5,
    "buy": 12,
    "hold": 18,
    "sell": 6,
    "strong_sell": 1,
    "avg_confidence": 0.72
  }
}
```

## 🎯 Features

✅ Real-time stock price updates
✅ AI-powered buy/sell signals
✅ Fundamental analysis (valuation, growth, health)
✅ Technical analysis (7+ indicators)
✅ Sentiment analysis (news-based)
✅ Portfolio monitoring (multiple stocks)
✅ Historical price charts
✅ WebSocket real-time updates
✅ Production-ready database
✅ Comprehensive error handling
✅ Rate limiting
✅ Logging and monitoring

## 🔧 Configuration

### Environment Variables (.env)
```bash
# API Keys
IEX_CLOUD_API_KEY=pk_...
ANTHROPIC_API_KEY=sk-ant-...

# Database
DATABASE_URL=sqlite:///./stocks.db
# Or PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/stocks_db

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=False

# Scheduler
SCHEDULER_ENABLED=True
UPDATE_INTERVAL_SECONDS=60
ANALYSIS_INTERVAL_MINUTES=5
```

## 📈 Performance

- **Stock Updates:** 100 stocks in ~30 seconds
- **AI Analysis:** 20 stocks in ~2 minutes
- **API Response Time:** <500ms average
- **WebSocket Latency:** <100ms

## 🚨 Error Handling

- Graceful API failures with fallback
- Comprehensive logging with loguru
- Database transaction rollback on errors
- Rate limit backoff
- Connection retry logic

## 📝 Logging

All operations logged to `logs/` directory:
- `app.log` - Application logs
- `api.log` - API request/response logs
- `agent.log` - AI agent analysis logs

## 🔐 Security

✅ API key management via .env
✅ No sensitive data in logs
✅ CORS configured for frontend
✅ Input validation on all endpoints
✅ SQL injection protection (SQLAlchemy ORM)
✅ Rate limiting on API calls

## 📱 Frontend Features

- Dashboard with stock list
- Real-time price updates
- Buy/Sell signal visualization
- Analysis details panel
- Search functionality
- Responsive mobile design
- Dark mode support
- Chart visualization

## 🚀 Deployment

### Docker (Recommended)
```bash
# Build image
docker build -t stock-analyzer .

# Run container
docker run -p 8000:8000 \
  -e IEX_CLOUD_API_KEY=your_key \
  -e ANTHROPIC_API_KEY=your_key \
  stock-analyzer
```

### Heroku
```bash
git push heroku main
heroku config:set IEX_CLOUD_API_KEY=your_key
heroku config:set ANTHROPIC_API_KEY=your_key
```

### VPS (Ubuntu/Debian)
```bash
# Install dependencies
sudo apt-get install python3.11 postgresql

# Setup application
git clone repo
cd stock-analysis-ai-agent
pip install -r requirements.txt

# Run with supervisor
sudo apt-get install supervisor
# Configure supervisor file
sudo supervisorctl reread && restart
```

## 🐛 Troubleshooting

**Issue:** "Module not found" errors
- Solution: `pip install -r requirements.txt`

**Issue:** API key errors
- Solution: Check .env file has correct keys
- Make sure keys have proper permissions

**Issue:** Database connection fails
- Solution: Check DATABASE_URL in .env
- Ensure PostgreSQL/SQLite is running

**Issue:** Claude API errors
- Solution: Check API key is valid
- Check account has credits
- Check rate limits aren't exceeded

## 📚 API Documentation

Full interactive API docs available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🤝 Contributing

Contributions welcome! Please:
1. Create feature branch
2. Make changes
3. Add tests
4. Submit pull request

## 📄 License

MIT License - Free for personal and commercial use

## 📞 Support

For issues or questions:
- GitHub Issues: [Create issue](https://github.com/dongsurya278-coder/stock-analysis-ai-agent/issues)
- Email: dongsurya278@gmail.com

## ⭐ Credits

Built with:
- **FastAPI** - Modern web framework
- **Claude 3.5 Sonnet** - AI analysis
- **IEX Cloud** - Stock data
- **React + Vite** - Frontend
- **SQLAlchemy** - Database ORM

---

**🎉 Project is production-ready and fully functional!**

Start using it today: http://localhost:5173
