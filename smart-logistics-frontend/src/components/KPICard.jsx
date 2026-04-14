import { motion } from "framer-motion";
import { TrendingUp, TrendingDown } from "lucide-react";

export function KPI({ title, value, color, trend, percentage }) {
  const isPositive = trend === 'up';
  
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02, y: -2 }}
      whileTap={{ scale: 0.98 }}
      className="bg-dark-card p-6 rounded-xl shadow-card hover:shadow-hover transition-all duration-300 border border-border-color relative overflow-hidden"
    >
      {/* Gradient overlay */}
      <div className={`absolute inset-0 bg-gradient-to-br opacity-10 pointer-events-none ${
        color === 'primary' ? 'from-primary to-transparent' :
        color === 'success' ? 'from-success to-transparent' :
        color === 'danger' ? 'from-danger to-transparent' :
        'from-info to-transparent'
      }`} />
      
      <div className="relative z-10">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h3 className="text-text-secondary text-sm font-medium">{title}</h3>
            <div className="flex items-center mt-2 space-x-2">
              {trend && (
                <div className={`flex items-center space-x-1 text-xs font-medium ${
                  isPositive ? 'text-success' : 'text-danger'
                }`}>
                  {isPositive ? (
                    <TrendingUp className="w-3 h-3" />
                  ) : (
                    <TrendingDown className="w-3 h-3" />
                  )}
                  <span>{percentage}%</span>
                </div>
              )}
            </div>
          </div>
          
          <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
            color === 'primary' ? 'bg-primary/20' :
            color === 'success' ? 'bg-success/20' :
            color === 'danger' ? 'bg-danger/20' :
            'bg-info/20'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              color === 'primary' ? 'bg-primary' :
              color === 'success' ? 'bg-success' :
              color === 'danger' ? 'bg-danger' :
              'bg-info'
            }`} />
          </div>
        </div>
        
        <p className={`text-3xl font-bold leading-tight ${
          color === 'primary' ? 'text-primary' :
          color === 'success' ? 'text-success' :
          color === 'danger' ? 'text-danger' :
          color === 'info' ? 'text-info' :
          'text-text-primary'
        }`}>
          {value}
        </p>
      </div>
    </motion.div>
  );
}