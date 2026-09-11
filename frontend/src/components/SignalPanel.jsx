import React, { useEffect } from 'react'
import { useStockStore } from '../store/stockStore'
import { AlertCircle, TrendingUp, CheckCircle } from 'lucide-react'

function SignalPanel() {
  const { signals, fetchStrongBuySignals } = useStockStore()

  useEffect(() => {
    fetchStrongBuySignals()
  }, [])

  const getSignalColor = (signal) => {
    switch (signal.signal_strength) {
      case 'strong_buy':
        return 'signal-strong-buy'
      case 'buy':
        return 'signal-buy'
      case 'hold':
        return 'signal-hold'
      case 'sell':
        return 'signal-sell'
      case 'strong_sell':
        return 'signal-strong-sell'
      default:
        return ''
    }
  }

  return (
    <div className="glass-effect rounded-xl p-6">
      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
        <AlertCircle className="w-5 h-5 text-yellow-400" />
        Active Buy Signals
      </h3>

      {signals.length === 0 ? (
        <p className="text-slate-400 text-sm text-center py-8">
          No active signals yet
        </p>
      ) : (
        <div className="space-y-3">
          {signals.slice(0, 5).map((signal) => (
            <div
              key={signal.id}
              className={`p-3 rounded-lg ${getSignalColor(signal)}`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold text-white">{signal.symbol}</p>
                  <p className="text-xs text-slate-300 capitalize">
                    {signal.signal_strength.replace('_', ' ')}
                  </p>
                </div>
                <div className="text-right">
                  <p className="text-sm font-bold">
                    {(signal.confidence_score * 100).toFixed(0)}%
                  </p>
                  <CheckCircle className="w-4 h-4 text-green-400 mt-1" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default SignalPanel
