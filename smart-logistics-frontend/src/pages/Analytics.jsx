import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import DemandHeatmap from '../components/DemandHeatmap'
import ClusterVisualization from '../components/ClusterVisualization'
import RevenueByState from '../components/RevenueByState'
import SupplyDemandComparison from '../components/SupplyDemandComparison'

const Analytics = () => {
  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-white">Analytics</h1>
          <p className="text-gray-400 mt-1">Deep insights into demand patterns and supply chains</p>
        </div>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <DemandHeatmap />
        <ClusterVisualization />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <RevenueByState />
        <SupplyDemandComparison />
      </div>
    </div>
  )
}

export default Analytics
