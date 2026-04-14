import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  AlertTriangle, 
  TrendingUp, 
  Package, 
  CheckCircle,
  Info,
  Filter,
  Search,
  Download,
  RefreshCw
} from 'lucide-react'

const Alerts = () => {
  const [alerts, setAlerts] = useState([])
  const [filteredAlerts, setFilteredAlerts] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filterLevel, setFilterLevel] = useState('all')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchAlerts()
  }, [])

  useEffect(() => {
    filterAlerts()
  }, [alerts, searchQuery, filterLevel])

  const fetchAlerts = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/alerts')
      const data = await response.json()
      setAlerts(data)
    } catch (error) {
      console.error('Failed to fetch alerts:', error)
      // Use sample data as fallback
      setAlerts([
        {
          id: 1,
          state: 'Tamil Nadu',
          product: 'Veshti',
          gap: 34.2,
          level: 'CRITICAL',
          revenue: 1575000,
          suggestion: 'Urgent restock by 1,204 units',
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          state: 'Punjab',
          product: 'Veshti',
          gap: 3.1,
          level: 'SAFE',
          revenue: 90000,
          suggestion: 'No action needed',
          timestamp: new Date().toISOString()
        },
        {
          id: 3,
          state: 'Maharashtra',
          product: 'Salwar Kameez',
          gap: 18.5,
          level: 'WARNING',
          revenue: 2080000,
          suggestion: 'Increase stock by 800 units',
          timestamp: new Date().toISOString()
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  const filterAlerts = () => {
    let filtered = alerts

    // Filter by level
    if (filterLevel !== 'all') {
      filtered = filtered.filter(alert => alert.level.toLowerCase() === filterLevel)
    }

    // Filter by search query
    if (searchQuery) {
      filtered = filtered.filter(alert => 
        alert.state.toLowerCase().includes(searchQuery.toLowerCase()) ||
        alert.product.toLowerCase().includes(searchQuery.toLowerCase())
      )
    }

    setFilteredAlerts(filtered)
  }

  const getAlertIcon = (level) => {
    switch (level) {
      case 'CRITICAL': return AlertTriangle
      case 'WARNING': return TrendingUp
      case 'INFO': return Info
      case 'SAFE': return CheckCircle
      default: return Package
    }
  }

  const getAlertColor = (level) => {
    switch (level) {
      case 'CRITICAL': return 'alert-critical'
      case 'WARNING': return 'alert-warning'
      case 'INFO': return 'alert-info'
      case 'SAFE': return 'alert-success'
      default: return 'bg-gray-700'
    }
  }

  const getLevelColor = (level) => {
    switch (level) {
      case 'CRITICAL': return 'text-critical'
      case 'WARNING': return 'text-warning'
      case 'INFO': return 'text-info'
      case 'SAFE': return 'text-success'
      default: return 'text-gray-300'
    }
  }

  const formatCurrency = (value) => {
    return `₹${(value / 100000).toFixed(1)}L`
  }

  const getRelativeTime = (timestamp) => {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now - date
    const diffMins = Math.floor(diffMs / 60000)
    
    if (diffMins < 60) return `${diffMins} minutes ago`
    const diffHours = Math.floor(diffMins / 60)
    if (diffHours < 24) return `${diffHours} hours ago`
    const diffDays = Math.floor(diffHours / 24)
    return `${diffDays} days ago`
  }

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white">Alerts Dashboard</h1>
          <p className="text-gray-400 mt-1">Real-time supply chain alerts and recommendations</p>
        </div>
        <div className="flex items-center space-x-4">
          <button
            onClick={fetchAlerts}
            disabled={loading}
            className="flex items-center space-x-2 px-4 py-2 bg-gray-700 text-white rounded-lg hover:bg-gray-600 transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
          <button className="flex items-center space-x-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/80 transition-colors">
            <Download className="w-4 h-4" />
            <span>Export</span>
          </button>
        </div>
      </motion.div>

      {/* Filters */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.1 }}
        className="card"
      >
        <div className="flex flex-col lg:flex-row gap-4">
          <div className="flex-1">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                placeholder="Search by state or product..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary placeholder-gray-400"
              />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Filter className="w-5 h-5 text-gray-400" />
            <select
              value={filterLevel}
              onChange={(e) => setFilterLevel(e.target.value)}
              className="bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="all">All Levels</option>
              <option value="critical">Critical</option>
              <option value="warning">Warning</option>
              <option value="info">Info</option>
              <option value="safe">Safe</option>
            </select>
          </div>
        </div>
      </motion.div>

      {/* Alert Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {[
          { level: 'CRITICAL', count: alerts.filter(a => a.level === 'CRITICAL').length, color: 'critical' },
          { level: 'WARNING', count: alerts.filter(a => a.level === 'WARNING').length, color: 'warning' },
          { level: 'INFO', count: alerts.filter(a => a.level === 'INFO').length, color: 'info' },
          { level: 'SAFE', count: alerts.filter(a => a.level === 'SAFE').length, color: 'success' }
        ].map((stat) => (
          <motion.div
            key={stat.level}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.2 }}
            className={`card p-4 border-l-4 border-${stat.color}`}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className={`text-${stat.color} text-sm font-medium`}>{stat.level}</p>
                <p className="text-2xl font-bold text-white mt-1">{stat.count}</p>
              </div>
              {React.createElement(getAlertIcon(stat.level), { className: `w-8 h-8 text-${stat.color} opacity-50` })}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Alerts Table */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="card"
      >
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-700">
                <th className="text-left py-3 px-4 text-gray-400 font-medium">State</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Product</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Gap %</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Level</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Revenue</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Action</th>
                <th className="text-left py-3 px-4 text-gray-400 font-medium">Time</th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence>
                {filteredAlerts.map((alert) => {
                  const Icon = getAlertIcon(alert.level)
                  return (
                    <motion.tr
                      key={alert.id}
                      initial={{ opacity: 0, x: -20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 20 }}
                      className={`border-b border-gray-700 hover:bg-gray-700/50 transition-colors ${alert.level === 'CRITICAL' ? 'animate-pulse-glow' : ''}`}
                    >
                      <td className="py-3 px-4">
                        <span className="text-white font-medium">{alert.state}</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-gray-300">{alert.product}</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className={`font-semibold ${alert.gap > 0 ? 'text-critical' : 'text-success'}`}>
                          {alert.gap > 0 ? '+' : ''}{alert.gap.toFixed(1)}%
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <div className="flex items-center space-x-2">
                          <Icon className={`w-4 h-4 ${getLevelColor(alert.level)}`} />
                          <span className={`text-sm font-medium ${getLevelColor(alert.level)}`}>
                            {alert.level}
                          </span>
                        </div>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-white">{formatCurrency(alert.revenue)}</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-300">{alert.suggestion}</span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-sm text-gray-400">{getRelativeTime(alert.timestamp)}</span>
                      </td>
                    </motion.tr>
                  )
                })}
              </AnimatePresence>
            </tbody>
          </table>
          
          {filteredAlerts.length === 0 && (
            <div className="text-center py-8">
              <Package className="w-12 h-12 mx-auto mb-4 text-gray-500" />
              <p className="text-gray-400">No alerts found matching your criteria</p>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  )
}

export default Alerts
