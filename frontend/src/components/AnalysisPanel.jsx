import React, { useEffect, useState } from 'react'
import { BarChart3, TrendingUp } from 'lucide-react'
import api from '../api/client'

function AnalysisPanel({ stock }) {
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('fundamentals')

  useEffect(() => {
    fetchAnalysis()
  }, [stock.symbol])

  const fetchAnalysis = async () => {
    setLoading(true)
    try {
      const [fundamentals, technical, sentiment] = await Promise.all([
        api.get(`/analysis/${stock.symbol}/fundamentals`),
        api.get(`/analysis/${stock.symbol}/technical`),
        api.get(`/analysis/${stock.symbol}/sentiment`),
      ])

      setAnalysis({
        fundamentals: fundamentals.data,
        technical: technical.data,
        sentiment: sentiment.data,
      })
    } catch (error) {
      console.error('Error fetching analysis:', error)
    } finally {
      setLoading(false)
    }
  }

  const renderFundamentals = () => (
    <div className="space-y-2 text-sm">
      {analysis?.fundamentals ? (
        <>
          <div className="flex justify-between">
            <span className="text-slate-400">P/E Ratio:</span>
            <span className="font-semibold">
              {analysis.fundamentals.pe_ratio?.toFixed(2) || 'N/A'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">EPS:</span>
            <span className="font-semibold">
              ${analysis.fundamentals.eps?.toFixed(2) || 'N/A'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">ROE:</span>
            <span className="font-semibold">
              {analysis.fundamentals.roe?.toFixed(2) || 'N/A'}%
            </span>
          </div>
        </>
      ) : (
        <p className="text-slate-400">Loading fundamentals...</p>
      )}
    </div>
  )

  const renderTechnical = () => (
    <div className="space-y-2 text-sm">
      {analysis?.technical ? (
        <>
          <div className="flex justify-between">
            <span className="text-slate-400">RSI:</span>
            <span className="font-semibold">
              {analysis.technical.rsi?.toFixed(2) || 'N/A'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">MA50:</span>
            <span className="font-semibold">
              ${analysis.technical.ma50?.toFixed(2) || 'N/A'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Support:</span>
            <span className="font-semibold">
              ${analysis.technical.support?.toFixed(2) || 'N/A'}
            </span>
          </div>
        </>
      ) : (
        <p className="text-slate-400">Loading technical data...</p>
      )}
    </div>
  )

  const renderSentiment = () => (
    <div className="space-y-2 text-sm">
      {analysis?.sentiment ? (
        <>
          <div className="flex justify-between">
            <span className="text-slate-400">Sentiment:</span>
            <span className={`font-semibold ${
              analysis.sentiment.sentiment_label === 'positive'
                ? 'text-green-400'
                : analysis.sentiment.sentiment_label === 'negative'
                  ? 'text-red-400'
                  : 'text-yellow-400'
            }`}>
              {analysis.sentiment.sentiment_label?.toUpperCase() || 'N/A'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Score:</span>
            <span className="font-semibold">
              {analysis.sentiment.sentiment_score?.toFixed(2) || 'N/A'}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">News Count:</span>
            <span className="font-semibold">
              {analysis.sentiment.recent_news_count || 0}
            </span>
          </div>
        </>
      ) : (
        <p className="text-slate-400">Loading sentiment...</p>
      )}
    </div>
  )

  if (!stock) return null

  return (
    <div className="glass-effect rounded-xl p-6">
      <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
        <BarChart3 className="w-5 h-5" />
        {stock.symbol} Analysis
      </h3>

      {/* Tab Navigation */}
      <div className="flex gap-2 mb-4 border-b border-slate-700">
        {['fundamentals', 'technical', 'sentiment'].map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-3 py-2 text-sm font-medium border-b-2 transition-colors ${
              activeTab === tab
                ? 'border-blue-500 text-blue-400'
                : 'border-transparent text-slate-400 hover:text-slate-300'
            }`}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {loading ? (
        <div className="text-center py-4">
          <div className="w-6 h-6 rounded-full border-3 border-blue-500 border-t-transparent animate-spin mx-auto"></div>
        </div>
      ) : activeTab === 'fundamentals' ? (
        renderFundamentals()
      ) : activeTab === 'technical' ? (
        renderTechnical()
      ) : (
        renderSentiment()
      )}
    </div>
  )
}

export default AnalysisPanel
