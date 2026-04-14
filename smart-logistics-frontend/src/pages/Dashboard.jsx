import { KPI } from "../components/KPICard";
import { BarChart, Bar, XAxis, YAxis, Tooltip, LineChart, Line, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import { motion } from "framer-motion";
import { TrendingUp, TrendingDown, AlertTriangle, CheckCircle, Clock, Brain, Sparkles } from "lucide-react";
import AIAssistant from "../components/AIAssistant";
import SDGImpact from "../components/SDGImpact";

const ordersData = [
  { name: "Jan", orders: 400 },
  { name: "Feb", orders: 800 },
  { name: "Mar", orders: 600 },
  { name: "Apr", orders: 900 },
  { name: "May", orders: 750 },
  { name: "Jun", orders: 1100 },
];

const revenueData = [
  { name: "Jan", revenue: 2400 },
  { name: "Feb", revenue: 1398 },
  { name: "Mar", revenue: 9800 },
  { name: "Apr", revenue: 3908 },
  { name: "May", revenue: 4800 },
  { name: "Jun", revenue: 3800 },
];

const distributionData = [
  { name: 'Delivered', value: 65, color: '#22C55E' },
  { name: 'In Transit', value: 20, color: '#3B82F6' },
  { name: 'Delayed', value: 10, color: '#FACC15' },
  { name: 'Overstock', value: 5, color: '#38BDF8' },
];

const liveActivity = [
  {
    id: 1,
    type: 'critical',
    title: 'Critical: TN needs stock urgently',
    description: 'Shortage: 1,200 units',
    time: '2 min ago',
    icon: AlertTriangle
  },
  {
    id: 2,
    type: 'warning',
    title: 'Warning: Punjab overstock',
    description: 'Excess: 500 units',
    time: '5 min ago',
    icon: AlertTriangle
  },
  {
    id: 3,
    type: 'success',
    title: 'Good: Kerala stable',
    description: 'Optimal levels',
    time: '12 min ago',
    icon: CheckCircle
  },
  {
    id: 4,
    type: 'info',
    title: 'Processing: Delhi shipment',
    description: 'In transit: 300 units',
    time: '18 min ago',
    icon: Clock
  }
];

export default function Dashboard() {
  return (
    <div>
      {/* TAILWIND TEST */}
      <div className="bg-red-500 text-white p-6 m-4">
        Tailwind Working Test - This should be RED with WHITE text
      </div>
      
      {/* ACTUAL DASHBOARD */}
      <div className="min-h-screen bg-bg-primary">
      {/* Centered Container */}
      <div className="max-w-7xl mx-auto p-6">
        
        {/* Header */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-text-primary mb-2 flex items-center space-x-2">
                <span>Smart Logistics Dashboard</span>
                <div className="bg-gradient-to-r from-primary to-info text-white text-xs px-2 py-1 rounded-full font-semibold">
                  🏆 GSC 2026
                </div>
              </h1>
              <p className="text-text-secondary">
                AI-powered supply chain intelligence with Gemini & Firebase
              </p>
            </div>
            <div className="flex items-center space-x-2">
              <div className="bg-green-500/20 text-green-500 px-3 py-1 rounded-full text-sm font-medium flex items-center space-x-1">
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span>Live</span>
              </div>
              <div className="bg-primary/20 text-primary px-3 py-1 rounded-full text-sm font-medium">
                AI Enhanced
              </div>
            </div>
          </div>
        </motion.div>

        {/* KPI Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card hover:shadow-card-hover transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-primary" />
              </div>
              <div className="flex items-center text-green-500 text-sm">
                <TrendingUp className="w-4 h-4 mr-1" />
                <span className="font-medium">12.5%</span>
              </div>
            </div>
            <h3 className="text-text-secondary text-sm font-medium mb-1">Total Orders</h3>
            <p className="text-3xl font-bold text-text-primary">12,340</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card hover:shadow-card-hover transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-success/20 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-6 h-6 text-success" />
              </div>
              <div className="flex items-center text-green-500 text-sm">
                <TrendingUp className="w-4 h-4 mr-1" />
                <span className="font-medium">8.3%</span>
              </div>
            </div>
            <h3 className="text-text-secondary text-sm font-medium mb-1">Revenue</h3>
            <p className="text-3xl font-bold text-text-primary">8.4M</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card hover:shadow-card-hover transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-info/20 rounded-xl flex items-center justify-center">
                <Clock className="w-6 h-6 text-info" />
              </div>
              <div className="flex items-center text-red-500 text-sm">
                <TrendingDown className="w-4 h-4 mr-1" />
                <span className="font-medium">2.1%</span>
              </div>
            </div>
            <h3 className="text-text-secondary text-sm font-medium mb-1">In Transit</h3>
            <p className="text-3xl font-bold text-text-primary">340</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card hover:shadow-card-hover transition-shadow"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 bg-danger/20 rounded-xl flex items-center justify-center">
                <AlertTriangle className="w-6 h-6 text-danger" />
              </div>
              <div className="flex items-center text-red-500 text-sm">
                <TrendingUp className="w-4 h-4 mr-1" />
                <span className="font-medium">15.7%</span>
              </div>
            </div>
            <h3 className="text-text-secondary text-sm font-medium mb-1">Alerts</h3>
            <p className="text-3xl font-bold text-text-primary">23</p>
          </motion.div>
        </div>

        {/* Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Total Orders Chart */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.5 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-text-primary">Total Orders</h2>
              <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-primary" />
              </div>
            </div>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={ordersData}>
                  <XAxis 
                    dataKey="name" 
                    stroke="#64748B" 
                    tick={{ fill: "#64748B", fontSize: 12 }}
                  />
                  <YAxis 
                    stroke="#64748B" 
                    tick={{ fill: "#64748B", fontSize: 12 }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: "#1E293B", 
                      border: "1px solid #334155",
                      borderRadius: "8px",
                      color: "#F1F5F9"
                    }} 
                  />
                  <Bar 
                    dataKey="orders" 
                    fill="#3B82F6" 
                    radius={[8, 8, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* Revenue Growth Chart */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.6 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-text-primary">Revenue Growth</h2>
              <div className="w-10 h-10 bg-success/20 rounded-xl flex items-center justify-center">
                <TrendingUp className="w-5 h-5 text-success" />
              </div>
            </div>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={revenueData}>
                  <XAxis 
                    dataKey="name" 
                    stroke="#64748B" 
                    tick={{ fill: "#64748B", fontSize: 12 }}
                  />
                  <YAxis 
                    stroke="#64748B" 
                    tick={{ fill: "#64748B", fontSize: 12 }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: "#1E293B", 
                      border: "1px solid #334155",
                      borderRadius: "8px",
                      color: "#F1F5F9"
                    }} 
                  />
                  <Line 
                    type="monotone" 
                    dataKey="revenue" 
                    stroke="#22C55E" 
                    strokeWidth={3}
                    dot={{ fill: "#22C55E", strokeWidth: 2, r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </motion.div>
        </div>

        {/* AI Assistant & Distribution Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          {/* Distribution Overview */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.7 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-text-primary">Distribution Overview</h2>
              <div className="w-10 h-10 bg-info/20 rounded-xl flex items-center justify-center">
                <Clock className="w-5 h-5 text-info" />
              </div>
            </div>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={distributionData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {distributionData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: "#1E293B", 
                      border: "1px solid #334155",
                      borderRadius: "8px",
                      color: "#F1F5F9"
                    }} 
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </motion.div>

          {/* AI Assistant */}
          <AIAssistant />
        </div>

        {/* Live Activity & SDG Impact Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Live Activity */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.8 }}
            className="bg-card-bg p-6 rounded-2xl shadow-card"
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold text-text-primary">Live Activity</h2>
              <div className="w-10 h-10 bg-warning/20 rounded-xl flex items-center justify-center">
                <div className="w-3 h-3 bg-warning rounded-full animate-pulse"></div>
              </div>
            </div>
            <div className="space-y-3 max-h-64 overflow-y-auto">
              {liveActivity.map((activity) => {
                const Icon = activity.icon;
                return (
                  <motion.div
                    key={activity.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className={`flex items-start space-x-3 p-3 rounded-xl border-l-4 ${
                      activity.type === 'critical' ? 'bg-danger/10 border-danger' :
                      activity.type === 'warning' ? 'bg-warning/10 border-warning' :
                      activity.type === 'success' ? 'bg-success/10 border-success' :
                      'bg-info/10 border-info'
                    }`}
                  >
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0 ${
                      activity.type === 'critical' ? 'bg-danger/20' :
                      activity.type === 'warning' ? 'bg-warning/20' :
                      activity.type === 'success' ? 'bg-success/20' :
                      'bg-info/20'
                    }`}>
                      <Icon className={`w-4 h-4 ${
                        activity.type === 'critical' ? 'text-danger' :
                        activity.type === 'warning' ? 'text-warning' :
                        activity.type === 'success' ? 'text-success' :
                        'text-info'
                      }`} />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className={`text-sm font-medium ${
                        activity.type === 'critical' ? 'text-danger' :
                        activity.type === 'warning' ? 'text-warning' :
                        activity.type === 'success' ? 'text-success' :
                        'text-info'
                      }`}>
                        {activity.title}
                      </p>
                      <p className="text-xs text-text-muted mt-1">{activity.description}</p>
                      <p className="text-xs text-text-secondary mt-1">{activity.time}</p>
                    </div>
                  </motion.div>
                );
              })}
            </div>
          </motion.div>

          {/* SDG Impact */}
          <SDGImpact />
        </div>
      </div>
      </div>
    </div>
  );
}