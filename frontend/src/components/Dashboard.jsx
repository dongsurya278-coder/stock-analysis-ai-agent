import React, { useEffect } from 'react'
import { useStockStore } from '../store/stockStore'
import StockList from './StockList'
import SignalPanel from './SignalPanel'
import AnalysisPanel from './AnalysisPanel'

function Dashboard() {
  const { selectedStock, setSelectedStock, fetchSignals } = useStockStore()

  useEffect(() => {
    fetchSignals()
    const interval = setInterval(fetchSignals, 60000) // Update every minute
    return () => clearInterval(interval)
  }, [])

  return (
    <main className="max-w-7xl mx-auto px-4 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Stock List - Main Content */}
        <div className="lg:col-span-2">
          <StockList onSelectStock={setSelectedStock} />
        </div>

        {/* Signals & Analysis - Sidebar */}
        <div className="space-y-6">
          <SignalPanel />
          {selectedStock && <AnalysisPanel stock={selectedStock} />}
        </div>
      </div>
    </main>
  )
}

export default Dashboard
