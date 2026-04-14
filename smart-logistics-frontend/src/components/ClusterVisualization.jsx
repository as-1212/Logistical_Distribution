import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts'

const ClusterVisualization = () => {
  const [data, setData] = useState([])

  useEffect(() => {
    // Generate sample cluster data
    const clusterData = [
      // High Demand / Under-supplied (Cluster 0)
      { demand: 85, supply: 0.6, gap: 35, cluster: 0, state: 'Tamil Nadu', product: 'Veshti' },
      { demand: 78, supply: 0.7, gap: 28, cluster: 0, state: 'Maharashtra', product: 'Salwar Kameez' },
      { demand: 92, supply: 0.5, gap: 42, cluster: 0, state: 'Kerala', product: 'Saree' },
      
      // High Demand / Well-supplied (Cluster 1)
      { demand: 88, supply: 1.2, gap: 8, cluster: 1, state: 'Karnataka', product: 'Veshti' },
      { demand: 75, supply: 1.1, gap: 5, cluster: 1, state: 'Gujarat', product: 'Dhoti' },
      { demand: 82, supply: 1.3, gap: 3, cluster: 1, state: 'Delhi', product: 'Kurta' },
      
      // Low Demand / Over-supplied (Cluster 2)
      { demand: 25, supply: 2.1, gap: -15, cluster: 2, state: 'Punjab', product: 'Veshti' },
      { demand: 35, supply: 1.8, gap: -12, cluster: 2, state: 'Rajasthan', product: 'Saree' },
      { demand: 20, supply: 2.5, gap: -18, cluster: 2, state: 'Haryana', product: 'Salwar Kameez' },
      
      // Moderate Demand / Balanced (Cluster 3)
      { demand: 55, supply: 0.9, gap: 12, cluster: 3, state: 'UP', product: 'Dhoti' },
      { demand: 48, supply: 1.0, gap: 8, cluster: 3, state: 'West Bengal', product: 'Kurta' },
      { demand: 62, supply: 0.8, gap: 15, cluster: 3, state: 'Odisha', product: 'Veshti' },
    ]
    
    setData(clusterData)
  }, [])

  const clusterColors = {
    0: '#EF4444', // Critical - High Demand / Under-supplied
    1: '#10B981', // Success - High Demand / Well-supplied
    2: '#06B6D4', // Info - Low Demand / Over-supplied
    3: '#F59E0B'  // Warning - Moderate Demand / Balanced
  }

  const clusterLabels = {
    0: 'High Demand / Under-supplied',
    1: 'High Demand / Well-supplied',
    2: 'Low Demand / Over-supplied',
    3: 'Moderate Demand / Balanced'
  }

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload
      return (
        <div className="bg-gray-800 p-3 rounded-lg border border-gray-700">
          <p className="text-white font-semibold">{data.state}</p>
          <p className="text-gray-300 text-sm">{data.product}</p>
          <p className="text-gray-400 text-xs mt-1">Demand Index: {data.demand}</p>
          <p className="text-gray-400 text-xs">Supply Ratio: {data.supply}</p>
          <p className="text-gray-400 text-xs">Gap %: {data.gap}%</p>
          <p className="text-xs mt-2" style={{ color: clusterColors[data.cluster] }}>
            {clusterLabels[data.cluster]}
          </p>
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
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-white">Cluster Analysis</h2>
        <p className="text-gray-400 text-sm mt-1">Demand vs Supply clustering visualization</p>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
          <XAxis 
            dataKey="demand" 
            name="Demand Index" 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
            label={{ value: 'Demand Index', position: 'insideBottom', offset: -5, fill: '#9CA3AF' }}
          />
          <YAxis 
            dataKey="supply" 
            name="Supply Ratio" 
            stroke="#9CA3AF"
            tick={{ fill: '#9CA3AF' }}
            label={{ value: 'Supply Ratio', angle: -90, position: 'insideLeft', fill: '#9CA3AF' }}
          />
          <Tooltip content={<CustomTooltip />} />
          
          {Object.entries(clusterColors).map(([cluster, color]) => (
            <Scatter
              key={cluster}
              name={clusterLabels[cluster]}
              data={data.filter(d => d.cluster === parseInt(cluster))}
              fill={color}
              fillOpacity={0.7}
              strokeWidth={2}
              stroke={color}
            />
          ))}
        </ScatterChart>
      </ResponsiveContainer>
      
      {/* Legend */}
      <div className="grid grid-cols-2 gap-4 mt-6">
        {Object.entries(clusterLabels).map(([cluster, label]) => (
          <div key={cluster} className="flex items-center space-x-3">
            <div 
              className="w-4 h-4 rounded-full"
              style={{ backgroundColor: clusterColors[cluster] }}
            />
            <span className="text-sm text-gray-300">{label}</span>
          </div>
        ))}
      </div>
    </motion.div>
  )
}

export default ClusterVisualization
