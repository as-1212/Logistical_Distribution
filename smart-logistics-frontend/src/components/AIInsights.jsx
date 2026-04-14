import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { 
  Brain, 
  TrendingUp, 
  ArrowRight, 
  Zap,
  Target,
  BarChart3
} from 'lucide-react'

const AIInsights = () => {
  const [insights, setInsights] = useState([])

  useEffect(() => {
    // Generate sample AI insights
    const sampleInsights = [
      {
        id: 1,
        type: 'opportunity',
        title: 'Increase Stock in South',
        description: 'Tamil Nadu and Kerala show 34% demand growth',
        impact: 'High',
        action: 'Increase stock by 2,500 units'
      },
      {
        id: 2,
        type: 'optimization',
        title: 'Reduce Overstock in North',
        description: 'Punjab has 45% excess inventory',
        impact: 'Medium',
        action: 'Redistribute 1,200 units'
      },
      {
        id: 3,
        type: 'alert',
        title: 'Critical Shortage in West',
        description: 'Maharashtra demand exceeds supply by 28%',
        impact: 'Critical',
        action: 'Urgent restock needed'
      }
    ]
    setInsights(sampleInsights)
  }, [])

  const getImpactColor = (impact) => {
    switch (impact) {
      case 'Critical': return 'text-critical bg-critical/10'
      case 'High': return 'text-warning bg-warning/10'
      case 'Medium': return 'text-info bg-info/10'
      default: return 'text-success bg-success/10'
    }
  }

  const getTypeIcon = (type) => {
    switch (type) {
      case 'opportunity': return TrendingUp
      case 'optimization': return BarChart3
      case 'alert': return Target
      default: return Brain
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, delay: 0.5 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Brain className="w-5 h-5 text-primary" />
          <h2 className="text-lg font-semibold text-white">AI Insights</h2>
        </div>
        <button className="text-xs text-primary hover:text-primary/80 transition-colors">
          View All
        </button>
      </div>
      
      <div className="space-y-3">
        {insights.map((insight) => {
          const Icon = getTypeIcon(insight.type)
          return (
            <motion.div
              key={insight.id}
              whileHover={{ scale: 1.02 }}
              className="p-3 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-all cursor-pointer"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center space-x-2">
                  <Icon className="w-4 h-4 text-primary" />
                  <h3 className="text-sm font-medium text-white">
                    {insight.title}
                  </h3>
                </div>
                <span className={`text-xs px-2 py-1 rounded-full ${getImpactColor(insight.impact)}`}>
                  {insight.impact}
                </span>
              </div>
              
              <p className="text-xs text-gray-400 mb-2">
                {insight.description}
              </p>
              
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-300">
                  {insight.action}
                </span>
                <ArrowRight className="w-3 h-3 text-gray-400" />
              </div>
            </motion.div>
          )
        })}
      </div>
      
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        className="w-full mt-4 flex items-center justify-center space-x-2 bg-primary text-white py-2 px-4 rounded-lg hover:bg-primary/80 transition-colors"
      >
        <Zap className="w-4 h-4" />
        <span className="text-sm font-medium">Auto Optimize Supply</span>
      </motion.button>
    </motion.div>
  )
}

export default AIInsights
