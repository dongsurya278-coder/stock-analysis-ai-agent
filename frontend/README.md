# Stock Analysis AI Agent Frontend

Modern React dashboard for AI-powered stock analysis.

## Setup

```bash
npm install
npm run dev
```

## Build

```bash
npm run build
npm run preview
```

## Environment Variables

Create `.env.local`:
```
VITE_API_URL=http://localhost:8000
```

## Features

- 📊 Real-time stock dashboard
- 📈 Interactive charts
- 🤖 AI-generated signals
- 📱 Responsive design
- ⚡ Real-time WebSocket updates

## API Integration

Connects to:
- `/api/stocks/` - Stock data
- `/api/signals/` - Buy/Sell signals
- `/api/analysis/{symbol}` - Analysis data
- `/ws/signals` - Real-time updates
