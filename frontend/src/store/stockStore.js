import create from 'zustand'
import api from '../api/client'

export const useStockStore = create((set, get) => ({
  stocks: [],
  signals: [],
  selectedStock: null,
  filter: 'all', // all, strong_buy, buy, hold, sell
  loading: false,
  error: null,

  fetchTopStocks: async () => {
    set({ loading: true })
    try {
      const response = await api.get('/stocks')
      set({ stocks: response.data.data, loading: false })
    } catch (error) {
      set({ error: error.message, loading: false })
    }
  },

  fetchStockDetail: async (symbol) => {
    try {
      const response = await api.get(`/stocks/${symbol}`)
      set({ selectedStock: response.data })
      return response.data
    } catch (error) {
      set({ error: error.message })
      throw error
    }
  },

  fetchSignals: async () => {
    try {
      const response = await api.get('/signals')
      set({ signals: response.data.data })
    } catch (error) {
      set({ error: error.message })
    }
  },

  fetchStrongBuySignals: async () => {
    try {
      const response = await api.get('/signals/strong-buy')
      set({ signals: response.data.data })
    } catch (error) {
      set({ error: error.message })
    }
  },

  setFilter: (filter) => set({ filter }),
  setSelectedStock: (stock) => set({ selectedStock: stock }),
}))
