import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { 
  AlertTriangle, 
  TrendingUp, 
  Package, 
  MapPin,
  CheckCircle,
  Clock
} from 'lucide-react'

const ActivityFeed = () => {
  const [activities, setActivities] = useState([])

  useEffect(() => {
    // Generate sample activities
    const sampleActivities = [
      {
        id: 1,
        type: 'critical',
        icon: AlertTriangle,
        message: 'Tamil Nadu needs 1200 units urgently',
        timestamp: '2 minutes ago',
        color: 'text-critical'
      },
      {
        id: 2,
        type: 'info',
        icon: Package,
        message: 'Punjab has excess stock of Veshti',
        timestamp: '5 minutes ago',
        color: 'text-info'
      },
      {
        id: 3,
        type: 'success',
        icon: CheckCircle,
        message: 'Kerala supply stable - no action needed',
        timestamp: '8 minutes ago',
        color: 'text-success'
      },
      {
        id: 4,
        type: 'warning',
        icon: TrendingUp,
        message: 'Maharashtra demand increased by 25%',
        timestamp: '12 minutes ago',
        color: 'text-warning'
      },
      {
        id: 5,
        type: 'info',
        icon: MapPin,
        message: 'New route optimized for Delhi region',
        timestamp: '15 minutes ago',
        color: 'text-info'
      }
    ]
    setActivities(sampleActivities)

    // Simulate real-time updates
    const interval = setInterval(() => {
      const newActivity = {
        id: Date.now(),
        type: ['critical', 'warning', 'info', 'success'][Math.floor(Math.random() * 4)],
        icon: [AlertTriangle, TrendingUp, Package, MapPin][Math.floor(Math.random() * 4)],
        message: [
          'Demand spike detected in Gujarat',
          'Supply route optimized for Karnataka',
          'Low stock alert for Rajasthan',
          'New order batch processed for UP'
        ][Math.floor(Math.random() * 4)],
        timestamp: 'Just now',
        color: ['text-critical', 'text-warning', 'text-info', 'text-success'][Math.floor(Math.random() * 4)]
      }
      
      setActivities(prev => [newActivity, ...prev.slice(0, 4)])
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: 0.4 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-white">Live Activity</h2>
        <div className="flex items-center space-x-1">
          <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
          <span className="text-xs text-gray-400">Live</span>
        </div>
      </div>
      
      <div className="space-y-3 max-h-64 overflow-y-auto">
        <AnimatePresence>
          {activities.map((activity) => (
            <motion.div
              key={activity.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.3 }}
              className="flex items-start space-x-3 p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors"
            >
              <activity.icon className={`w-4 h-4 ${activity.color} mt-0.5 flex-shrink-0`} />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-white truncate">
                  {activity.message}
                </p>
                <div className="flex items-center space-x-1 mt-1">
                  <Clock className="w-3 h-3 text-gray-500" />
                  <span className="text-xs text-gray-400">
                    {activity.timestamp}
                  </span>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
    </motion.div>
  )
}

export default ActivityFeed
