import React from 'react'
import { TrendingUp, BarChart3, AlertCircle, RefreshCw } from 'lucide-react'
import { useStockStore } from '../store/stockStore'

function Header() {
  const { loading, fetchTopStocks, fetchSignals } = useStockStore()

  const handleRefresh = async () => {
    await Promise.all([fetchTopStocks(), fetchSignals()])
  }

  return (
    <header className="glass-effect border-b border-slate-700 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-blue-500 rounded-lg">
            <BarChart3 className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold gradient-text">Stock AI Agent</h1>
            <p className="text-sm text-slate-400">Real-time US Stock Analysis</p>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <button
            onClick={handleRefresh}
            disabled={loading}
            className="flex items-center gap-2 px-4 py-2 bg-blue-500 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg transition-colors"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <div className="text-right">
            <p className="text-sm text-slate-400">Last Updated</p>
            <p className="text-xs text-slate-500">{new Date().toLocaleTimeString()}</p>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
