import React from 'react'
import { motion } from 'framer-motion'
import { Wifi, WifiOff } from 'lucide-react'

const RealTimeIndicator = ({ connected }) => {
  return (
    <div className="flex items-center space-x-2">
      <motion.div
        animate={{ scale: connected ? [1, 1.2, 1] : 1 }}
        transition={{ duration: 2, repeat: connected ? Infinity : 0 }}
        className="flex items-center space-x-2"
      >
        {connected ? (
          <>
            <Wifi className="w-4 h-4 text-success" />
            <span className="text-xs text-success">Live</span>
          </>
        ) : (
          <>
            <WifiOff className="w-4 h-4 text-critical" />
            <span className="text-xs text-critical">Offline</span>
          </>
        )}
      </motion.div>
    </div>
  )
}

export default RealTimeIndicator
