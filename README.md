# Stock Analysis AI Agent - Complete Implementation
## 🤖 AI-Powered Stock Analysis Platform

### ✨ Features

✅ **AI Agent Analysis**
- Claude AI integration for comprehensive stock analysis
- Automatic fundamental, technical, and sentiment analysis
- Real-time buy/sell signals with confidence scores

✅ **Real-time Data**
- IEX Cloud API for market data
- Yahoo Finance integration for historical data
- Live WebSocket updates

✅ **Analysis Types**
- Fundamental Analysis (P/E, EPS, Revenue, Debt ratios, ROE, ROA)
- Technical Analysis (RSI, MACD, Moving Averages, Bollinger Bands)
- Sentiment Analysis (News sentiment scoring)

✅ **Trading Signals**
- Automated signal generation (Strong Buy/Buy/Hold/Sell/Strong Sell)
- Confidence scoring (0-100%)
- Entry/Target/Stop Loss prices

✅ **Dashboard**
- Real-time stock list
- Signal panel with color-coded recommendations
- Detailed analysis views
- Portfolio tracking

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL or SQLite
- API Keys:
  - [IEX Cloud](https://iexcloud.io) - Stock data
  - [Anthropic Claude](https://console.anthropic.com) - AI analysis

### 1️⃣ Backend Setup (5 minutes)

```bash
# Clone repository
git clone https://github.com/dongsurya278-coder/stock-analysis-ai-agent.git
cd stock-analysis-ai-agent/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys:
# - IEX_CLOUD_API_KEY
# - ANTHROPIC_API_KEY
# - DATABASE_URL (optional, defaults to SQLite)

# Run migrations (automatic)
python -m app.main

# Start server
uvicorn app.main:app --reload
```

**Backend URL:** http://localhost:8000
**API Docs:** http://localhost:8000/docs

### 2️⃣ Frontend Setup (3 minutes)

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend URL:** http://localhost:5173

---

## 📊 API Endpoints

### Stocks
```
GET  /api/stocks              - Get all stocks
GET  /api/stocks/{symbol}     - Get stock details
GET  /api/stocks/{symbol}/history - Get price history
POST /api/stocks/update/{symbol}  - Update stock price
```

### Analysis
```
GET  /api/analysis/{symbol}/fundamentals - Fundamental analysis
GET  /api/analysis/{symbol}/technical    - Technical analysis
GET  /api/analysis/{symbol}/sentiment    - Sentiment analysis
GET  /api/analysis/{symbol}/full         - Complete analysis
```

### Signals
```
GET  /api/signals                - Get all active signals
GET  /api/signals/strong-buy     - Get strong buy signals
GET  /api/signals/{symbol}       - Get signal for stock
POST /api/signals/generate/{symbol} - Generate new signal
GET  /api/signals/stats/summary  - Get signals summary
```

### WebSocket
```
WS   /ws/signals    - Real-time signal updates
WS   /ws/live       - Live stock data streaming
```

---

## 🤖 How the AI Agent Works

### 1. Data Collection
- Fetches current price, volume, and fundamentals
- Retrieves 3-month historical price data
- Gathers latest news articles

### 2. Analysis
```
┌─────────────────────────────────────┐
│   Stock Data Collection             │
└──────────────┬──────────────────────┘
               ↓
   ┌───────────────────────────┐
   │  Claude AI Analysis       │
   │  (Comprehensive Review)   │
   └───────────┬───────────────┘
               ↓
   ┌───────────────────────────┐
   │  Signal Generation        │
   │  (Buy/Sell Decision)      │
   └───────────┬───────────────┘
               ↓
   ┌───────────────────────────┐
   │  Database Storage         │
   │  + WebSocket Broadcast    │
   └───────────────────────────┘
```

### 3. Signal Scoring
- **Fundamental Score (45%)** - P/E, Growth, Health
- **Technical Score (35%)** - RSI, MACD, Moving Averages
- **Sentiment Score (20%)** - News sentiment

---

## 📈 Example Usage

### Get Stock Analysis
```bash
curl http://localhost:8000/api/stocks/AAPL
```

Response:
```json
{
  "status": "success",
  "data": {
    "symbol": "AAPL",
    "price": 189.95,
    "change": 2.45,
    "changePercent": 1.31,
    "fundamentals": {...},
    "signal": {
      "signal_strength": "buy",
      "confidence_score": 0.82,
      "entry_price": 188.50,
      "target_price": 210.00,
      "stop_loss": 175.00
    }
  }
}
```

### Generate Signal
```bash
curl -X POST http://localhost:8000/api/signals/generate/AAPL
```

### Subscribe to WebSocket
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/signals');
ws.onmessage = (event) => {
  console.log('Signal update:', JSON.parse(event.data));
};
```

---

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/stock_db

# API Keys (Required)
IEX_CLOUD_API_KEY=pk_...
ANTHROPIC_API_KEY=sk-...

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### Database Setup (Optional PostgreSQL)
```bash
# Create database
createdb stock_ai_agent

# Update .env
DATABASE_URL=postgresql://user:password@localhost:5432/stock_ai_agent
```

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### View Logs
```bash
tail -f logs/app.log
```

### Database Stats
```bash
curl http://localhost:8000/api/signals/stats/summary
```

---

## 🚀 Deployment

### Docker
```bash
# Build image
docker build -t stock-ai-agent .

# Run container
docker run -p 8000:8000 --env-file .env stock-ai-agent
```

### Heroku
```bash
heroku create stock-ai-agent
heroku config:set IEX_CLOUD_API_KEY=...
heroku config:set ANTHROPIC_API_KEY=...
git push heroku main
```

---

## 🔗 API Response Examples

### Strong Buy Signal
```json
{
  "signal_strength": "strong_buy",
  "confidence_score": 0.92,
  "entry_price": 150.00,
  "target_price": 180.00,
  "stop_loss": 140.00,
  "reasoning": "Stock showing strong momentum with positive fundamentals and bullish technical setup"
}
```

### Full Analysis
```json
{
  "symbol": "TSLA",
  "price": 242.84,
  "fundamentals": {
    "peRatio": 52.3,
    "eps": 4.65,
    "revenue": 81462000000,
    "valuation_score": 35
  },
  "technical_score": 72,
  "sentiment": {
    "score": 0.65,
    "label": "positive"
  }
}
```

---

## ⚙️ Scheduled Tasks

- **Every 60 seconds:** Update stock prices
- **Every 5 minutes:** Run AI agent analysis on top 20 stocks
- **Every hour:** Generate fresh signals

---

## 🐛 Troubleshooting

### API Key Issues
```bash
# Check if keys are set
echo $IEX_CLOUD_API_KEY
echo $ANTHROPIC_API_KEY

# Test IEX API
curl "https://cloud.iexapis.com/stable/stock/AAPL/quote?token=YOUR_KEY"
```

### Database Connection
```bash
# Test PostgreSQL
psql -U user -d stock_ai_agent -c "SELECT 1;"

# Reset database
rm stock_analysis.db  # SQLite
```

### Port Already in Use
```bash
# Use different port
uvicorn app.main:app --port 8001
```

---

## 📚 Tech Stack

**Backend:**
- FastAPI - Web framework
- SQLAlchemy - ORM
- Claude AI - Analysis engine
- APScheduler - Background tasks
- WebSocket - Real-time updates

**Frontend:**
- React 18 - UI framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Recharts - Charting
- Axios - API client

**Data Sources:**
- IEX Cloud - Stock market data
- Yahoo Finance - Historical data
- News APIs - Market sentiment

---

## 📝 License

MIT License - Free to use and modify

---

## 🤝 Support

For issues or questions:
1. Check the [API Documentation](http://localhost:8000/docs)
2. Review [GitHub Issues](https://github.com/dongsurya278-coder/stock-analysis-ai-agent/issues)
3. Create a new issue with details

---

## 🎯 Roadmap

- [ ] Advanced portfolio optimization
- [ ] Risk management strategies
- [ ] Multi-timeframe analysis
- [ ] Custom alert notifications
- [ ] Mobile app
- [ ] Options analysis
- [ ] Cryptocurrency support

---

**Made with ❤️ by Dongsurya278 | Powered by Claude AI**
