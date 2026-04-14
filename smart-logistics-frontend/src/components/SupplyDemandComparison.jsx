import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const SupplyDemandComparison = () => {
  const [data, setData] = useState([])
  const [timeRange, setTimeRange] = useState('6months')

  useEffect(() => {
    // Generate sample supply-demand comparison data
    const comparisonData = [
      { month: 'Jan', supply: 4500, demand: 4800, optimal: 4650 },
      { month: 'Feb', supply: 4200, demand: 4600, optimal: 4400 },
      { month: 'Mar', supply: 4800, demand: 5200, optimal: 5000 },
      { month: 'Apr', supply: 5100, demand: 4900, optimal: 5000 },
      { month: 'May', supply: 5300, demand: 5500, optimal: 5400 },
      { month: 'Jun', supply: 4900, demand: 5100, optimal: 5000 },
      { month: 'Jul', supply: 5200, demand: 5300, optimal: 5250 },
      { month: 'Aug', supply: 5500, demand: 5400, optimal: 5450 },
      { month: 'Sep', supply: 5800, demand: 6000, optimal: 5900 },
      { month: 'Oct', supply: 6200, demand: 6100, optimal: 6150 },
      { month: 'Nov', supply: 6500, demand: 6800, optimal: 6650 },
      { month: 'Dec', supply: 7000, demand: 7200, optimal: 7100 }
    ]
    
    // Filter based on time range
    const filteredData = timeRange === '3months' 
      ? comparisonData.slice(-3)
      : timeRange === '6months'
      ? comparisonData.slice(-6)
      : comparisonData
    
    setData(filteredData)
  }, [timeRange])

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-gray-800 p-3 rounded-lg border border-gray-700">
          <p className="text-white font-semibold">{data.month}</p>
          <p className="text-blue-400 text-sm">Supply: {data.supply.toLocaleString()}</p>
          <p className="text-green-400 text-sm">Demand: {data.demand.toLocaleString()}</p>
          <p className="text-yellow-400 text-sm">Optimal: {data.optimal.toLocaleString()}</p>
          <p className="text-gray-300 text-xs mt-1">
            Gap: {data.demand - data.supply > 0 ? '+' : ''}{(data.demand - data.supply).toLocaleString()}
          </p>
        </div>
      )
    }
    return null
  }

  const calculateEfficiency = () => {
    if (data.length === 0) return 0
    const totalSupply = data.reduce((sum, item) => sum + item.supply, 0)
    const totalDemand = data.reduce((sum, item) => sum + item.demand, 0)
    return Math.round((totalSupply / totalDemand) * 100)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-white">Supply vs Demand</h2>
          <p className="text-gray-400 text-sm mt-1">Supply chain efficiency analysis</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-right">
            <p className="text-sm text-gray-400">Efficiency Rate</p>
            <p className={`text-lg font-bold ${calculateEfficiency() >= 95 ? 'text-success' : calculateEfficiency() >= 85 ? 'text-warning' : 'text-critical'}`}>
              {calculateEfficiency()}%
            </p>
          </div>
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="bg-gray-700 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
          >
            <option value="3months">Last 3 Months</option>
            <option value="6months">Last 6 Months</option>
            <option value="12months">Last 12 Months</option>
          </select>
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
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ color: '#9CA3AF' }}
          />
          <Line 
            type="monotone" 
            dataKey="supply" 
            stroke="#3B82F6" 
            strokeWidth={2}
            dot={{ fill: '#3B82F6', strokeWidth: 2 }}
            animationDuration={1000}
          />
          <Line 
            type="monotone" 
            dataKey="demand" 
            stroke="#10B981" 
            strokeWidth={2}
            dot={{ fill: '#10B981', strokeWidth: 2 }}
            animationDuration={1000}
          />
          <Line 
            type="monotone" 
            dataKey="optimal" 
            stroke="#F59E0B" 
            strokeWidth={2}
            strokeDasharray="5 5"
            dot={{ fill: '#F59E0B', strokeWidth: 2 }}
            animationDuration={1000}
          />
        </LineChart>
      </ResponsiveContainer>
      
      {/* Key Metrics */}
      <div className="grid grid-cols-3 gap-4 mt-6">
        <div className="text-center p-3 bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-400">Avg Supply</p>
          <p className="text-lg font-bold text-blue-400">
            {data.length > 0 ? Math.round(data.reduce((sum, item) => sum + item.supply, 0) / data.length).toLocaleString() : 0}
          </p>
        </div>
        <div className="text-center p-3 bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-400">Avg Demand</p>
          <p className="text-lg font-bold text-green-400">
            {data.length > 0 ? Math.round(data.reduce((sum, item) => sum + item.demand, 0) / data.length).toLocaleString() : 0}
          </p>
        </div>
        <div className="text-center p-3 bg-gray-700/50 rounded-lg">
          <p className="text-sm text-gray-400">Avg Gap</p>
          <p className={`text-lg font-bold ${data.length > 0 && data.reduce((sum, item) => sum + (item.demand - item.supply), 0) / data.length > 0 ? 'text-critical' : 'text-success'}`}>
            {data.length > 0 ? Math.round(data.reduce((sum, item) => sum + (item.demand - item.supply), 0) / data.length).toLocaleString() : 0}
          </p>
        </div>
      </div>
    </motion.div>
  )
}

export default SupplyDemandComparison
