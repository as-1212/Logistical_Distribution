import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ResponsiveContainer, Tooltip } from 'recharts'

const DemandHeatmap = () => {
  const [data, setData] = useState([])
  const [selectedProduct, setSelectedProduct] = useState('all')

  useEffect(() => {
    // Generate sample heatmap data
    const states = ['Tamil Nadu', 'Kerala', 'Karnataka', 'Maharashtra', 'Punjab', 'Gujarat']
    const products = ['Veshti', 'Saree', 'Dhoti', 'Salwar Kameez', 'Kurta']
    
    const heatmapData = states.map(state => {
      const rowData = { state }
      products.forEach(product => {
        // Generate demand index with some patterns
        let demand = Math.random() * 100
        if (state === 'Tamil Nadu' && product === 'Veshti') demand = 95
        if (state === 'Punjab' && product === 'Salwar Kameez') demand = 88
        if (state === 'Kerala' && product === 'Saree') demand = 82
        rowData[product] = Math.round(demand)
      })
      return rowData
    })
    
    setData(heatmapData)
  }, [])

  const getHeatColor = (value) => {
    if (value >= 80) return 'bg-critical/80'
    if (value >= 60) return 'bg-warning/80'
    if (value >= 40) return 'bg-info/80'
    return 'bg-success/80'
  }

  const products = ['Veshti', 'Saree', 'Dhoti', 'Salwar Kameez', 'Kurta']
  const filteredProducts = selectedProduct === 'all' ? products : [selectedProduct]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-xl font-semibold text-white">Demand Heatmap</h2>
          <p className="text-gray-400 text-sm mt-1">State vs Product demand analysis</p>
        </div>
        <select
          value={selectedProduct}
          onChange={(e) => setSelectedProduct(e.target.value)}
          className="bg-gray-700 text-white px-3 py-2 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="all">All Products</option>
          {products.map(product => (
            <option key={product} value={product}>{product}</option>
          ))}
        </select>
      </div>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left py-3 px-4 text-gray-400 font-medium">State</th>
              {filteredProducts.map(product => (
                <th key={product} className="text-center py-3 px-4 text-gray-400 font-medium">
                  {product}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, index) => (
              <motion.tr
                key={row.state}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3, delay: index * 0.1 }}
                className="border-t border-gray-700"
              >
                <td className="py-3 px-4 text-white font-medium">
                  {row.state}
                </td>
                {filteredProducts.map(product => (
                  <td key={product} className="py-3 px-2 text-center">
                    <div
                      className={`w-full h-8 rounded flex items-center justify-center text-white font-semibold text-sm ${getHeatColor(row[product])}`}
                    >
                      {row[product]}
                    </div>
                  </td>
                ))}
              </motion.tr>
            ))}
          </tbody>
        </table>
      </div>
      
      {/* Legend */}
      <div className="flex items-center justify-center space-x-4 mt-6">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-success/80 rounded" />
          <span className="text-xs text-gray-400">Low (0-40)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-info/80 rounded" />
          <span className="text-xs text-gray-400">Medium (40-60)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-warning/80 rounded" />
          <span className="text-xs text-gray-400">High (60-80)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-critical/80 rounded" />
          <span className="text-xs text-gray-400">Very High (80-100)</span>
        </div>
      </div>
    </motion.div>
  )
}

export default DemandHeatmap
