import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const RevenueByState = () => {
  const [data, setData] = useState([])
  const [sortBy, setSortBy] = useState('revenue')

  useEffect(() => {
    // Generate sample revenue data
    const revenueData = [
      { state: 'Tamil Nadu', revenue: 15750000, orders: 4567 },
      { state: 'Maharashtra', revenue: 12500000, orders: 3890 },
      { state: 'Karnataka', revenue: 9800000, orders: 3123 },
      { state: 'Gujarat', revenue: 8900000, orders: 2876 },
      { state: 'Kerala', revenue: 8700000, orders: 2765 },
      { state: 'Delhi', revenue: 7600000, orders: 2345 },
      { state: 'Punjab', revenue: 6700000, orders: 1987 },
      { state: 'West Bengal', revenue: 5400000, orders: 1654 }
    ]
    
    setData(revenueData)
  }, [])

  useEffect(() => {
    // Sort data based on selected criteria
    const sortedData = [...data].sort((a, b) => {
      if (sortBy === 'revenue') return b.revenue - a.revenue
      if (sortBy === 'orders') return b.orders - a.orders
      return 0
    })
    setData(sortedData)
  }, [sortBy])

  const formatCurrency = (value) => {
    return `₹${(value / 100000).toFixed(1)}L`
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-gray-800 p-3 rounded-lg border border-gray-700">
          <p className="text-white font-semibold">{data.state}</p>
          <p className="text-gray-300 text-sm">Revenue: {formatCurrency(data.revenue)}</p>
          <p className="text-gray-300 text-sm">Orders: {data.orders.toLocaleString()}</p>
        </div>
      )
    }
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-white">Revenue by State</h2>
          <p className="text-gray-400 text-sm mt-1">Top performing states</p>
        </div>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="bg-gray-700 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="revenue">Sort by Revenue</option>
          <option value="orders">Sort by Orders</option>
        </select>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} layout="horizontal">
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            type="number" 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
            tickFormatter={formatCurrency}
          />
          <YAxis 
            dataKey="state" 
            type="category" 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
            width={80}
          />
          <Tooltip content={<CustomTooltip />} />
          <Bar 
            dataKey="revenue" 
            fill="#3B82F6" 
            radius={[0, 8, 8, 0]}
            animationDuration={1000}
          />
        </BarChart>
      </ResponsiveContainer>
      
      {/* Top States Summary */}
      <div className="mt-6 space-y-3">
        <h3 className="text-sm font-semibold text-gray-400">Top 3 States</h3>
        {data.slice(0, 3).map((state, index) => (
          <div key={state.state} className="flex items-center justify-between p-3 bg-gray-700/50 rounded-lg">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-primary/20 rounded-full flex items-center justify-center">
                <span className="text-primary font-bold text-sm">{index + 1}</span>
              </div>
              <div>
                <p className="text-white font-medium">{state.state}</p>
                <p className="text-gray-400 text-xs">{state.orders.toLocaleString()} orders</p>
              </div>
            </div>
            <div className="text-right">
              <p className="text-white font-semibold">{formatCurrency(state.revenue)}</p>
              <p className="text-success text-xs">+{Math.floor(Math.random() * 20 + 5)}%</p>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}

export default RevenueByState
