import { motion } from "framer-motion";
import { Search, Bell, User, Filter, Download, Settings } from "lucide-react";

export default function Navbar() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-card border-b border-border shadow-soft"
    >
      <div className="flex items-center justify-between px-6 py-4">
        {/* Left Section - Search */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.2 }}
          className="flex items-center space-x-4 flex-1"
        >
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-textSecondary w-5 h-5" />
            <motion.input
              whileFocus={{ scale: 1.02 }}
              className="w-full pl-10 pr-4 py-2.5 bg-accent/20 border border-border rounded-xl text-textPrimary placeholder-textSecondary focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all"
              placeholder="Search products, states, or alerts..."
            />
          </div>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center space-x-2 px-4 py-2.5 bg-accent/20 border border-border rounded-xl hover:bg-accent/30 transition-all"
          >
            <Filter className="w-4 h-4 text-textSecondary" />
            <span className="text-sm font-medium text-textSecondary">Filters</span>
          </motion.button>
        </motion.div>

        {/* Right Section - Actions */}
        <div className="flex items-center space-x-3">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center space-x-2 px-4 py-2.5 bg-primary/10 border border-primary/30 rounded-xl hover:bg-primary/20 transition-all"
          >
            <Download className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Export</span>
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="relative flex items-center justify-center w-10 h-10 bg-accent/20 border border-border rounded-xl hover:bg-accent/30 transition-all"
          >
            <Bell className="w-5 h-5 text-textSecondary" />
            <motion.div 
              className="absolute top-0 right-0 w-3 h-3 bg-danger rounded-full"
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </motion.button>
          
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="flex items-center space-x-2 px-3 py-2 bg-accent/20 border border-border rounded-xl hover:bg-accent/30 transition-all"
          >
            <User className="w-4 h-4 text-textSecondary" />
            <span className="text-sm font-medium text-textSecondary">Admin</span>
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}