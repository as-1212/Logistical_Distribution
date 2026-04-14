import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { MapPin, TrendingUp, AlertTriangle, Package } from 'lucide-react'

const SupplyMap = () => {
  const [mapData, setMapData] = useState([])
  const [selectedState, setSelectedState] = useState(null)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    // Fetch map data from API
    const fetchMapData = async () => {
      try {
        const response = await fetch('/api/map')
        const data = await response.json()
        setMapData(data.states || [])
      } catch (error) {
        console.error('Failed to fetch map data:', error)
        // Use sample data as fallback
        setMapData([
          {
            name: 'Tamil Nadu',
            demandScore: 3.5,
            shortage: 1200,
            revenue: 15750000,
            status: 'high-demand',
            coordinates: [11.1271, 78.6569]
          },
          {
            name: 'Maharashtra',
            demandScore: 2.8,
            shortage: 800,
            revenue: 12500000,
            status: 'moderate-demand',
            coordinates: [19.0760, 72.8777]
          },
          {
            name: 'Kerala',
            demandScore: 1.2,
            shortage: -300,
            revenue: 8900000,
            status: 'balanced',
            coordinates: [10.8505, 76.2711]
          },
          {
            name: 'Punjab',
            demandScore: 0.8,
            shortage: -500,
            revenue: 6700000,
            status: 'overstock',
            coordinates: [31.1471, 75.3412]
          }
        ])
      }
    }

    fetchMapData()
  }, [])

  const getStatusColor = (status) => {
    switch (status) {
      case 'high-demand': return 'bg-critical/20 border-critical/50 text-critical'
      case 'moderate-demand': return 'bg-warning/20 border-warning/50 text-warning'
      case 'balanced': return 'bg-success/20 border-success/50 text-success'
      case 'overstock': return 'bg-info/20 border-info/50 text-info'
      default: return 'bg-gray-700 border-gray-600 text-gray-300'
    }
  }

  const getMapColor = (status) => {
    switch (status) {
      case 'high-demand': return '#EF4444'
      case 'moderate-demand': return '#F59E0B'
      case 'balanced': return '#10B981'
      case 'overstock': return '#06B6D4'
      default: return '#6B7280'
    }
  }

  const formatCurrency = (value) => {
    return `₹${(value / 100000).toFixed(1)}L`
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white">Supply Map</h1>
          <p className="text-gray-400 mt-1">Interactive demand visualization across India</p>
        </div>
        <select
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
        >
          <option value="all">All States</option>
          <option value="high-demand">High Demand</option>
          <option value="moderate-demand">Moderate Demand</option>
          <option value="balanced">Balanced</option>
          <option value="overstock">Overstock</option>
        </select>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="lg:col-span-2 card"
        >
          <div className="mb-4">
            <h2 className="text-xl font-semibold text-white">India Demand Map</h2>
            <p className="text-gray-400 text-sm mt-1">Click on states for detailed information</p>
          </div>
          
          {/* Simplified India Map */}
          <div className="relative bg-gray-800 rounded-lg p-8 h-96 overflow-hidden">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-gray-500 text-center">
                <MapPin className="w-16 h-16 mx-auto mb-4 opacity-50" />
                <p>Interactive Map Visualization</p>
                <p className="text-sm mt-2">States would be rendered here with real map library</p>
              </div>
            </div>
            
            {/* State Indicators */}
            <div className="absolute inset-0 pointer-events-none">
              {mapData.map((state, index) => (
                <div
                  key={state.name}
                  className="absolute transform -translate-x-1/2 -translate-y-1/2"
                  style={{
                    left: `${20 + (index * 15)}%`,
                    top: `${30 + (index * 10)}%`
                  }}
                >
                  <div
                    className="w-4 h-4 rounded-full animate-pulse"
                    style={{ backgroundColor: getMapColor(state.status) }}
                  />
                  <span className="text-xs text-white absolute top-5 left-1/2 transform -translate-x-1/2 whitespace-nowrap">
                    {state.name}
                  </span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Legend */}
          <div className="flex items-center justify-center space-x-6 mt-6">
            {[
              { status: 'high-demand', label: 'High Demand', color: 'critical' },
              { status: 'moderate-demand', label: 'Moderate', color: 'warning' },
              { status: 'balanced', label: 'Balanced', color: 'success' },
              { status: 'overstock', label: 'Overstock', color: 'info' }
            ].map((item) => (
              <div key={item.status} className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full bg-${item.color}`} />
                <span className="text-xs text-gray-400">{item.label}</span>
              </div>
            ))}
          </div>
        </motion.div>

        {/* State Details Panel */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
          className="space-y-4"
        >
          <div className="card">
            <h3 className="text-lg font-semibold text-white mb-4">State Details</h3>
            
            {selectedState ? (
              <div className="space-y-4">
                <div>
                  <h4 className="text-xl font-bold text-white">{selectedState.name}</h4>
                  <div className={`inline-block px-2 py-1 rounded-full text-xs mt-2 ${getStatusColor(selectedState.status)}`}>
                    {selectedState.status.replace('-', ' ').toUpperCase()}
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Demand Score</span>
                    <span className="text-white font-semibold">{selectedState.demandScore}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Shortage</span>
                    <span className={`font-semibold ${selectedState.shortage > 0 ? 'text-critical' : 'text-success'}`}>
                      {selectedState.shortage > 0 ? '+' : ''}{selectedState.shortage} units
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Revenue</span>
                    <span className="text-white font-semibold">{formatCurrency(selectedState.revenue)}</span>
                  </div>
                </div>
                
                <button className="w-full bg-primary text-white py-2 px-4 rounded-lg hover:bg-primary/80 transition-colors">
                  View Details
                </button>
              </div>
            ) : (
              <div className="text-center text-gray-400 py-8">
                <MapPin className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Click on a state to view details</p>
              </div>
            )}
          </div>

          {/* Quick Stats */}
          <div className="card">
            <h3 className="text-lg font-semibold text-white mb-4">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <AlertTriangle className="w-4 h-4 text-critical" />
                  <span className="text-sm text-gray-400">Critical States</span>
                </div>
                <span className="text-white font-semibold">
                  {mapData.filter(s => s.status === 'high-demand').length}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <Package className="w-4 h-4 text-info" />
                  <span className="text-sm text-gray-400">Overstock States</span>
                </div>
                <span className="text-white font-semibold">
                  {mapData.filter(s => s.status === 'overstock').length}
                </span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <TrendingUp className="w-4 h-4 text-success" />
                  <span className="text-sm text-gray-400">Balanced States</span>
                </div>
                <span className="text-white font-semibold">
                  {mapData.filter(s => s.status === 'balanced').length}
                </span>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default SupplyMap
