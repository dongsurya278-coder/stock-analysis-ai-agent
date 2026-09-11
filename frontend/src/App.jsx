import React, { useEffect, useState } from 'react'
import Dashboard from './components/Dashboard'
import Header from './components/Header'
import { Toaster } from 'react-hot-toast'
import { useStockStore } from './store/stockStore'

function App() {
  const [loading, setLoading] = useState(true)
  const { fetchTopStocks } = useStockStore()

  useEffect(() => {
    const initializeApp = async () => {
      try {
        await fetchTopStocks()
      } catch (error) {
        console.error('Error initializing app:', error)
      } finally {
        setLoading(false)
      }
    }

    initializeApp()
  }, [])

  return (
    <div className="min-h-screen bg-slate-900">
      <Header />
      {loading ? (
        <div className="flex items-center justify-center h-96">
          <div className="text-center">
            <div className="w-12 h-12 rounded-full border-4 border-blue-500 border-t-transparent animate-spin mx-auto mb-4"></div>
            <p className="text-slate-400">Loading Stock Data...</p>
          </div>
        </div>
      ) : (
        <Dashboard />
      )}
      <Toaster position="bottom-right" />
    </div>
  )
}

export default App
