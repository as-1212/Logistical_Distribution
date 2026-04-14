import { motion } from "framer-motion";
import { 
  LayoutDashboard, 
  BarChart3, 
  Map, 
  AlertTriangle, 
  Settings,
  Package,
  TrendingUp
} from "lucide-react";

export default function Sidebar() {
  const menuItems = [
    { icon: LayoutDashboard, label: 'Dashboard', active: true },
    { icon: BarChart3, label: 'Analytics', active: false },
    { icon: Map, label: 'Supply Map', active: false },
    { icon: AlertTriangle, label: 'Alerts', active: false },
    { icon: Settings, label: 'Settings', active: false },
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, x: -100 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, ease: "easeOut" }}
      className="w-72 bg-gradient-to-b from-card to-card/95 border-r border-border shadow-card flex flex-col"
    >
      {/* Logo Section */}
      <div className="p-6 border-b border-border">
        <motion.div 
          initial={{ scale: 0.8, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="flex items-center space-x-3"
        >
          <div className="w-10 h-10 bg-gradient-to-br from-primary to-primary/80 rounded-xl flex items-center justify-center shadow-glow">
            <Package className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-textPrimary">SmartAI</h1>
            <p className="text-xs text-textSecondary font-medium">Logistics Intelligence</p>
          </div>
        </motion.div>
      </div>
      
      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item, index) => {
            const Icon = item.icon;
            return (
              <motion.li
                key={item.label}
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.1 + index * 0.1 }}
                whileHover={{ scale: 1.02, x: 8 }}
                whileTap={{ scale: 0.98 }}
                className={`relative group cursor-pointer`}
              >
                <div className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-300 ${
                  item.active 
                    ? 'bg-gradient-to-r from-primary to-primary/80 text-white shadow-glow' 
                    : 'hover:bg-accent text-textSecondary hover:text-white'
                }`}>
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                  {item.active && (
                    <motion.div 
                      layoutId="activeIndicator"
                      className="absolute right-2 w-2 h-2 bg-white rounded-full"
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      transition={{ type: "spring" }}
                    />
                  )}
                </div>
                
                {/* Hover effect */}
                <div className="absolute inset-0 bg-gradient-to-r from-primary/20 to-info/20 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </motion.li>
            );
          })}
        </ul>
      </nav>

      {/* Bottom Stats */}
      <div className="p-6 border-t border-border">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="space-y-4"
        >
          <div className="flex items-center justify-between text-sm">
            <span className="text-textSecondary">System Status</span>
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-success rounded-full animate-pulse"></div>
              <span className="text-success font-medium">Online</span>
            </div>
          </div>
          
          <div className="flex items-center justify-between text-sm">
            <span className="text-textSecondary">Efficiency</span>
            <div className="flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-success" />
              <span className="text-success font-medium">94.2%</span>
            </div>
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
}