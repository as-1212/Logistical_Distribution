import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  Leaf, 
  Factory, 
  TrendingUp, 
  Recycle, 
  Globe, 
  Target,
  Award,
  BarChart3
} from 'lucide-react';

const SDGImpact = () => {
  const [impactData, setImpactData] = useState({
    carbonSaved: 1200,
    wasteReduced: 18,
    efficiencyIncreased: 25,
    regionsOptimized: 12,
    co2Prevented: 2400,
    resourcesSaved: 450
  });

  const [animatedValues, setAnimatedValues] = useState({
    carbonSaved: 0,
    wasteReduced: 0,
    efficiencyIncreased: 0,
    regionsOptimized: 0,
    co2Prevented: 0,
    resourcesSaved: 0
  });

  useEffect(() => {
    const timer = setTimeout(() => {
      setAnimatedValues(impactData);
    }, 500);
    return () => clearTimeout(timer);
  }, []);

  const sdgGoals = [
    {
      number: 12,
      title: "Responsible Consumption & Production",
      icon: Recycle,
      color: "text-green-500",
      bgColor: "bg-green-500/20",
      description: "Reducing waste through optimized inventory management"
    },
    {
      number: 9,
      title: "Industry, Innovation & Infrastructure",
      icon: Factory,
      color: "text-blue-500",
      bgColor: "bg-blue-500/20",
      description: "Building smart logistics systems with AI"
    },
    {
      number: 13,
      title: "Climate Action",
      icon: Leaf,
      color: "text-emerald-500",
      bgColor: "bg-emerald-500/20",
      description: "Reducing carbon footprint through efficient distribution"
    }
  ];

  const impactMetrics = [
    {
      label: "Carbon Saved",
      value: `${animatedValues.carbonSaved} kg`,
      icon: Leaf,
      color: "text-green-500",
      bgColor: "bg-green-500/10",
      change: "+15%",
      trend: "up"
    },
    {
      label: "Waste Reduced",
      value: `${animatedValues.wasteReduced}%`,
      icon: Recycle,
      color: "text-blue-500",
      bgColor: "bg-blue-500/10",
      change: "+8%",
      trend: "up"
    },
    {
      label: "Efficiency Increased",
      value: `${animatedValues.efficiencyIncreased}%`,
      icon: TrendingUp,
      color: "text-purple-500",
      bgColor: "bg-purple-500/10",
      change: "+12%",
      trend: "up"
    },
    {
      label: "CO₂ Prevented",
      value: `${animatedValues.co2Prevented} kg`,
      icon: Globe,
      color: "text-emerald-500",
      bgColor: "bg-emerald-500/10",
      change: "+22%",
      trend: "up"
    },
    {
      label: "Resources Saved",
      value: `${animatedValues.resourcesSaved} tons`,
      icon: BarChart3,
      color: "text-orange-500",
      bgColor: "bg-orange-500/10",
      change: "+18%",
      trend: "up"
    },
    {
      label: "Regions Optimized",
      value: animatedValues.regionsOptimized,
      icon: Target,
      color: "text-indigo-500",
      bgColor: "bg-indigo-500/10",
      change: "+3",
      trend: "up"
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.9 }}
      className="bg-card-bg rounded-2xl shadow-card p-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
            <Award className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-text-primary">SDG Impact Dashboard</h2>
            <p className="text-text-secondary text-sm">Sustainability metrics & achievements</p>
          </div>
        </div>
        <div className="bg-green-500/20 text-green-500 px-3 py-1 rounded-full text-sm font-medium">
          Live Impact
        </div>
      </div>

      {/* SDG Goals */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        {sdgGoals.map((goal, index) => {
          const Icon = goal.icon;
          return (
            <motion.div
              key={goal.number}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 1.0 + index * 0.1 }}
              className={`${goal.bgColor} border border-${goal.color}/20 rounded-xl p-4`}
            >
              <div className="flex items-start space-x-3">
                <div className={`w-12 h-12 ${goal.bgColor} rounded-lg flex items-center justify-center flex-shrink-0`}>
                  <Icon className={`w-6 h-6 ${goal.color}`} />
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-lg font-bold text-text-primary">SDG {goal.number}</span>
                  </div>
                  <h3 className="text-sm font-semibold text-text-primary mb-1">{goal.title}</h3>
                  <p className="text-xs text-text-secondary">{goal.description}</p>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Impact Metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-3 gap-4">
        {impactMetrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <motion.div
              key={metric.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.3 + index * 0.05 }}
              className={`${metric.bgColor} rounded-xl p-4 border border-${metric.color}/20`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className={`w-8 h-8 ${metric.bgColor} rounded-lg flex items-center justify-center`}>
                  <Icon className={`w-4 h-4 ${metric.color}`} />
                </div>
                <div className={`flex items-center text-xs font-medium ${
                  metric.trend === 'up' ? 'text-green-500' : 'text-red-500'
                }`}>
                  {metric.trend === 'up' ? '↑' : '↓'} {metric.change}
                </div>
              </div>
              <h3 className="text-text-secondary text-xs font-medium mb-1">{metric.label}</h3>
              <p className="text-2xl font-bold text-text-primary">{metric.value}</p>
            </motion.div>
          );
        })}
      </div>

      {/* Achievement Banner */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1.8 }}
        className="mt-6 bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-xl p-4"
      >
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center">
            <Award className="w-5 h-5 text-white" />
          </div>
          <div className="flex-1">
            <h3 className="text-green-500 font-semibold mb-1">🌍 UN SDG Contribution Achieved</h3>
            <p className="text-text-secondary text-sm">
              Your smart logistics system has contributed to 3 UN Sustainable Development Goals, 
              creating measurable environmental and social impact across {impactData.regionsOptimized} regions.
            </p>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

export default SDGImpact;
