import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const OrdersChart = () => {
  const [data, setData] = useState([])
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    // Generate sample data
    const sampleData = [
      { month: 'Jan', orders: 4000, revenue: 2400 },
      { month: 'Feb', orders: 3000, revenue: 1398 },
      { month: 'Mar', orders: 2000, revenue: 9800 },
      { month: 'Apr', orders: 2780, revenue: 3908 },
      { month: 'May', orders: 1890, revenue: 4800 },
      { month: 'Jun', orders: 2390, revenue: 3800 },
      { month: 'Jul', orders: 3490, revenue: 4300 },
      { month: 'Aug', orders: 4200, revenue: 5100 },
      { month: 'Sep', orders: 3800, revenue: 4700 },
      { month: 'Oct', orders: 5100, revenue: 6200 },
      { month: 'Nov', orders: 4800, revenue: 5900 },
      { month: 'Dec', orders: 6200, revenue: 7500 },
    ]
    setData(sampleData)
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: 0.1 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-white">Total Orders</h2>
          <p className="text-gray-400 text-sm mt-1">Monthly order trends</p>
        </div>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-gray-700 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="all">All Products</option>
          <option value="veshti">Veshti</option>
          <option value="saree">Saree</option>
          <option value="dhoti">Dhoti</option>
        </select>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="month" 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
          />
          <YAxis 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1F2937',
              border: '1px solid #374151',
              borderRadius: '8px',
              color: '#F3F4F6'
            }}
          />
          <Legend 
            wrapperStyle={{ color: '#9CA3AF' }}
          />
          <Bar 
            dataKey="orders" 
            fill="#3B82F6" 
            radius={[8, 8, 0, 0]}
            animationDuration={1000}
          />
        </BarChart>
      </ResponsiveContainer>
    </motion.div>
  )
}

export default OrdersChart
