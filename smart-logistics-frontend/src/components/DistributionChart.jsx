import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts'

const DistributionChart = () => {
  const [data, setData] = useState([])

  useEffect(() => {
    // Generate sample distribution data
    const sampleData = [
      { name: 'Delivered', value: 65, color: '#10B981' },
      { name: 'In Transit', value: 20, color: '#3B82F6' },
      { name: 'Delayed', value: 10, color: '#F59E0B' },
      { name: 'Overstock', value: 5, color: '#06B6D4' },
    ]
    setData(sampleData)
  }, [])

  const RADIAN = Math.PI / 180
  const renderCustomizedLabel = ({
    cx, cy, midAngle, innerRadius, outerRadius, percent
  }) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text 
        x={x} 
        y={y} 
        fill="white" 
        textAnchor={x > cx ? 'start' : 'end'} 
        dominantBaseline="central"
        className="text-sm font-semibold"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: 0.3 }}
      className="card"
    >
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">Distribution Overview</h2>
        <p className="text-gray-400 text-sm mt-1">Order status distribution</p>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={100}
            fill="#8884d8"
            dataKey="value"
            animationBegin={0}
            animationDuration={1000}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: '#1F2937',
              border: '1px solid #374151',
              borderRadius: '8px',
              color: '#F3F4F6'
            }}
            formatter={(value) => [`${value}%`, 'Percentage']}
          />
          <Legend 
            wrapperStyle={{ color: '#9CA3AF' }}
            verticalAlign="bottom"
            height={36}
          />
        </PieChart>
      </ResponsiveContainer>
      
      <div className="grid grid-cols-2 gap-4 mt-6">
        {data.map((item, index) => (
          <div key={index} className="flex items-center space-x-3">
            <div 
              className="w-3 h-3 rounded-full"
              style={{ backgroundColor: item.color }}
            />
            <span className="text-sm text-gray-300">{item.name}</span>
            <span className="text-sm font-semibold text-white ml-auto">
              {item.value}%
            </span>
          </div>
        ))}
      </div>
    </motion.div>
  )
}

export default DistributionChart
