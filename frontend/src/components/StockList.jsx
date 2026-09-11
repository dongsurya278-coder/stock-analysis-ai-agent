import React, { useEffect, useState } from 'react'
import { useStockStore } from '../store/stockStore'
import { TrendingUp, TrendingDown, Search } from 'lucide-react'
import api from '../api/client'

function StockList({ onSelectStock }) {
  const { stocks, loading, filter, setFilter } = useStockStore()
  const [filteredStocks, setFilteredStocks] = useState([])
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    let filtered = stocks

    if (searchTerm) {
      filtered = filtered.filter(
        (stock) =>
          stock.symbol.toLowerCase().includes(searchTerm.toLowerCase()) ||
          stock.company_name?.toLowerCase().includes(searchTerm.toLowerCase()),
      )
    }

    setFilteredStocks(filtered)
  }, [stocks, searchTerm, filter])

  if (loading) {
    return (
      <div className="glass-effect rounded-xl p-8 text-center">
        <div className="w-8 h-8 rounded-full border-4 border-blue-500 border-t-transparent animate-spin mx-auto"></div>
      </div>
    )
  }

  return (
    <div className="glass-effect rounded-xl p-6">
      <h2 className="text-xl font-bold mb-4">Top 100 US Stocks</h2>

      {/* Search Bar */}
      <div className="mb-4 relative">
        <Search className="absolute left-3 top-3 w-4 h-4 text-slate-400" />
        <input
          type="text"
          placeholder="Search stocks..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full pl-10 pr-4 py-2 bg-slate-800 border border-slate-700 rounded-lg focus:outline-none focus:border-blue-500 text-slate-100 placeholder-slate-500"
        />
      </div>

      {/* Stock Items */}
      <div className="space-y-2 max-h-96 overflow-y-auto">
        {filteredStocks.length === 0 ? (
          <p className="text-slate-400 text-center py-8">No stocks found</p>
        ) : (
          filteredStocks.map((stock) => (
            <StockCard
              key={stock.symbol}
              stock={stock}
              onClick={() => onSelectStock(stock)}
            />
          ))
        )}
      </div>
    </div>
  )
}

function StockCard({ stock, onClick }) {
  const change = stock.price?.change || 0
  const isPositive = change >= 0

  return (
    <div
      onClick={onClick}
      className="p-3 bg-slate-800 hover:bg-slate-700 rounded-lg cursor-pointer transition-colors border border-slate-700 hover:border-blue-500"
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="font-semibold">{stock.symbol}</p>
          <p className="text-xs text-slate-400">{stock.company_name || 'N/A'}</p>
        </div>
        <div className="text-right">
          <p className="font-bold">${stock.price?.price?.toFixed(2) || 'N/A'}</p>
          <p
            className={`text-xs flex items-center justify-end gap-1 ${
              isPositive ? 'text-green-400' : 'text-red-400'
            }`}
          >
            {isPositive ? (
              <TrendingUp className="w-3 h-3" />
            ) : (
              <TrendingDown className="w-3 h-3" />
            )}
            {Math.abs(change).toFixed(2)}%
          </p>
        </div>
      </div>
    </div>
  )
}

export default StockList
