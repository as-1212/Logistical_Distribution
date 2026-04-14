import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

const RevenueChart = () => {
  const [data, setData] = useState([])

  useEffect(() => {
    // Generate sample revenue data
    const sampleData = [
      { month: 'Jan', revenue: 4000000, growth: 5 },
      { month: 'Feb', revenue: 4200000, growth: 5 },
      { month: 'Mar', revenue: 3800000, growth: -9.5 },
      { month: 'Apr', revenue: 4500000, growth: 18.4 },
      { month: 'May', revenue: 5200000, growth: 15.6 },
      { month: 'Jun', revenue: 4800000, growth: -7.7 },
      { month: 'Jul', revenue: 5600000, growth: 16.7 },
      { month: 'Aug', revenue: 6200000, growth: 10.7 },
      { month: 'Sep', revenue: 5800000, growth: -6.5 },
      { month: 'Oct', revenue: 6800000, growth: 17.2 },
      { month: 'Nov', revenue: 7200000, growth: 5.9 },
      { month: 'Dec', revenue: 8500000, growth: 18.1 },
    ]
    setData(sampleData)
  }, [])

  const formatCurrency = (value) => {
    return `₹${(value / 100000).toFixed(1)}L`
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: 0.2 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-white">Revenue Trend</h2>
          <p className="text-gray-400 text-sm mt-1">Monthly revenue growth</p>
        </div>
        <div className="text-sm text-success">
          +12.5% YoY
        </div>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="month" 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
          />
          <YAxis 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
            tickFormatter={formatCurrency}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1F2937',
              border: '1px solid #374151',
              borderRadius: '8px',
              color: '#F3F4F6'
            }}
            formatter={(value) => [formatCurrency(value), 'Revenue']}
          />
          <Line 
            type="monotone" 
            dataKey="revenue" 
            stroke="#10B981" 
            strokeWidth={3}
            dot={{ fill: '#10B981', strokeWidth: 2 }}
            activeDot={{ r: 8 }}
            animationDuration={1500}
          />
        </LineChart>
      </ResponsiveContainer>
    </motion.div>
  )
}

export default RevenueChart
