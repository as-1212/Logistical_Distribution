#!/usr/bin/env python3
"""
Smart Logistics ML Engine
Integrates with the existing Python ML system and provides API endpoints
"""

import sys
import json
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class SmartLogisticsML:
    def __init__(self):
        self.data = None
        self.processed_data = None
        self.clusters = None
        self.scaler = StandardScaler()
        
    def load_data(self, data_input):
        """Load data from JSON input or CSV file"""
        if isinstance(data_input, str):
            # Assume it's a file path
            self.data = pd.read_csv(data_input)
        else:
            # Assume it's JSON data from API
            self.data = pd.DataFrame(data_input)
        
        return self.data
    
    def preprocess_data(self):
        """Preprocess the raw data"""
        df = self.data.copy()
        
        # Normalize column names
        df.columns = df.columns.str.strip().str.replace(' ', '_').str.upper()
        
        # Required columns
        required_cols = ['STATE', 'PRODUCT', 'UNITS_SOLD', 'SUPPLY_AVAILABLE', 'REVENUE']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Convert numeric columns
        numeric_cols = ['UNITS_SOLD', 'SUPPLY_AVAILABLE', 'REVENUE']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Calculate derived metrics
        df['DEMAND_GAP'] = df['UNITS_SOLD'] - df['SUPPLY_AVAILABLE']
        df['GAP_PCT'] = (df['DEMAND_GAP'] / df['UNITS_SOLD'] * 100).fillna(0)
        df['SHORTAGE_FLAG'] = df['DEMAND_GAP'] > 0
        
        self.processed_data = df
        return df
    
    def run_ai_analysis(self):
        """Run AI analysis including clustering and demand scoring"""
        if self.processed_data is None:
            raise ValueError("Data not preprocessed. Call preprocess_data() first.")
        
        # Aggregate by state and product
        agg_data = self.processed_data.groupby(['STATE', 'PRODUCT']).agg({
            'UNITS_SOLD': 'sum',
            'SUPPLY_AVAILABLE': 'sum',
            'REVENUE': 'sum',
            'GAP_PCT': 'mean',
            'DEMAND_GAP': 'sum'
        }).reset_index()
        
        # Calculate demand index (0-100 scale)
        agg_data['DEMAND_INDEX'] = self._calculate_demand_index(agg_data)
        
        # Calculate supply ratio
        agg_data['SUPPLY_RATIO'] = agg_data['SUPPLY_AVAILABLE'] / agg_data['UNITS_SOLD']
        agg_data['SUPPLY_RATIO'] = agg_data['SUPPLY_RATIO'].fillna(0)
        
        # Run K-means clustering
        features = ['DEMAND_INDEX', 'SUPPLY_RATIO', 'GAP_PCT']
        X = agg_data[features].values
        X_scaled = self.scaler.fit_transform(X)
        
        kmeans = KMeans(n_clusters=4, random_state=42)
        agg_data['CLUSTER'] = kmeans.fit_predict(X_scaled)
        
        # Label clusters
        agg_data['CLUSTER_LABEL'] = agg_data['CLUSTER'].apply(self._label_cluster)
        
        # Calculate recommended stock allocation
        agg_data = self._calculate_stock_allocation(agg_data)
        
        self.clusters = agg_data
        return agg_data
    
    def _calculate_demand_index(self, df):
        """Calculate demand index (0-100 scale)"""
        demand_index = []
        
        for product in df['PRODUCT'].unique():
            product_data = df[df['PRODUCT'] == product]
            max_sold = product_data['UNITS_SOLD'].max()
            
            for _, row in product_data.iterrows():
                if max_sold > 0:
                    index = (row['UNITS_SOLD'] / max_sold) * 100
                else:
                    index = 0
                demand_index.append(index)
        
        return demand_index
    
    def _label_cluster(self, cluster_id):
        """Label clusters based on characteristics"""
        cluster_labels = {
            0: 'High Demand / Under-supplied',
            1: 'High Demand / Well-supplied', 
            2: 'Low Demand / Over-supplied',
            3: 'Moderate Demand / Balanced'
        }
        return cluster_labels.get(cluster_id, 'Unknown')
    
    def _calculate_stock_allocation(self, df):
        """Calculate recommended stock allocation"""
        allocation_results = []
        
        for product in df['PRODUCT'].unique():
            product_data = df[df['PRODUCT'] == product].copy()
            total_demand_index = product_data['DEMAND_INDEX'].sum()
            total_supply = product_data['SUPPLY_AVAILABLE'].sum()
            
            if total_demand_index > 0:
                # Proportional allocation based on demand index
                product_data['RECOMMENDED_STOCK'] = (
                    (product_data['DEMAND_INDEX'] / total_demand_index) * total_supply
                ).round(0)
                
                # Calculate difference from current stock
                product_data['STOCK_VS_CURRENT'] = (
                    product_data['RECOMMENDED_STOCK'] - product_data['SUPPLY_AVAILABLE']
                ).round(0)
            else:
                product_data['RECOMMENDED_STOCK'] = product_data['SUPPLY_AVAILABLE']
                product_data['STOCK_VS_CURRENT'] = 0
            
            allocation_results.append(product_data)
        
        return pd.concat(allocation_results, ignore_index=True)
    
    def generate_alerts(self):
        """Generate alerts based on analysis"""
        if self.clusters is None:
            raise ValueError("Analysis not run. Call run_ai_analysis() first.")
        
        alerts = []
        
        for _, row in self.clusters.iterrows():
            gap_pct = row['GAP_PCT']
            supply_ratio = row['SUPPLY_RATIO']
            
            if gap_pct > 30:
                level = 'CRITICAL'
                color = '#EF4444'
            elif gap_pct > 10:
                level = 'WARNING'
                color = '#F59E0B'
            elif supply_ratio > 1.5:
                level = 'INFO'
                color = '#06B6D4'
            else:
                level = 'SAFE'
                color = '#10B981'
            
            suggestion = self._generate_suggestion(row, level)
            
            alert = {
                'id': len(alerts) + 1,
                'state': row['STATE'],
                'product': row['PRODUCT'],
                'gap_pct': round(gap_pct, 1),
                'level': level,
                'color': color,
                'revenue': int(row['REVENUE']),
                'suggestion': suggestion,
                'timestamp': datetime.now().isoformat()
            }
            
            alerts.append(alert)
        
        return alerts
    
    def _generate_suggestion(self, row, level):
        """Generate actionable suggestions"""
        if level == 'CRITICAL':
            return f"Urgent restock by {abs(int(row['DEMAND_GAP']))} units"
        elif level == 'WARNING':
            return f"Increase stock by {abs(int(row['DEMAND_GAP']))} units"
        elif level == 'INFO':
            return f"Excess stock - consider redistribution"
        else:
            return "No action needed"
    
    def generate_improvements(self, alerts):
        """Generate improvement suggestions"""
        improvements = []
        
        # Sort alerts by revenue impact
        critical_alerts = [a for a in alerts if a['level'] == 'CRITICAL']
        warning_alerts = [a for a in alerts if a['level'] == 'WARNING']
        info_alerts = [a for a in alerts if a['level'] == 'INFO']
        
        # High priority - critical shortages
        for alert in sorted(critical_alerts, key=lambda x: x['revenue'], reverse=True):
            improvements.append({
                'priority': 'High',
                'type': 'critical_shortage',
                'state': alert['state'],
                'product': alert['product'],
                'revenue_impact': alert['revenue'],
                'action': alert['suggestion']
            })
        
        # Medium priority - overstock
        for alert in sorted(info_alerts, key=lambda x: x['revenue'], reverse=True):
            improvements.append({
                'priority': 'Medium',
                'type': 'overstock',
                'state': alert['state'],
                'product': alert['product'],
                'revenue_impact': alert['revenue'],
                'action': 'Redirect excess inventory to high-demand regions'
            })
        
        return improvements
    
    def get_dashboard_summary(self):
        """Get summary data for dashboard"""
        if self.processed_data is None:
            return None
        
        total_orders = self.processed_data['UNITS_SOLD'].sum()
        total_revenue = self.processed_data['REVENUE'].sum()
        total_supply = self.processed_data['SUPPLY_AVAILABLE'].sum()
        
        # Calculate in-transit (simulate)
        in_transit = int(total_orders * 0.027)  # ~2.7% in transit
        
        # Get alerts count
        alerts = self.generate_alerts()
        alerts_count = len([a for a in alerts if a['level'] in ['CRITICAL', 'WARNING']])
        
        return {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'in_transit_orders': in_transit,
            'alerts_count': alerts_count,
            'overall_gap_pct': ((total_orders - total_supply) / total_orders * 100) if total_orders > 0 else 0
        }
    
    def get_map_data(self):
        """Get data for interactive map visualization"""
        if self.clusters is None:
            return []
        
        map_data = []
        
        for _, row in self.clusters.iterrows():
            # Calculate demand score (0-4 scale)
            demand_score = (row['DEMAND_INDEX'] / 100) * 4
            
            # Determine status
            if demand_score > 3.0:
                status = 'high-demand'
            elif demand_score > 1.5:
                status = 'moderate-demand'
            elif demand_score > 0.5:
                status = 'low-demand'
            else:
                status = 'negligible-demand'
            
            # Get coordinates (simplified - would use real geo data in production)
            coordinates = self._get_state_coordinates(row['STATE'])
            
            map_data.append({
                'state': row['STATE'],
                'demandScore': round(demand_score, 1),
                'shortage': int(row['DEMAND_GAP']),
                'revenue': int(row['REVENUE']),
                'status': status,
                'coordinates': coordinates
            })
        
        return map_data
    
    def _get_state_coordinates(self, state_name):
        """Get approximate coordinates for Indian states"""
        coordinates = {
            'Tamil Nadu': [11.1271, 78.6569],
            'Maharashtra': [19.0760, 72.8777],
            'Kerala': [10.8505, 76.2711],
            'Punjab': [31.1471, 75.3412],
            'Karnataka': [15.3173, 75.7139],
            'Gujarat': [22.2587, 71.1924],
            'Rajasthan': [27.0238, 74.2179],
            'Delhi': [28.7041, 77.1025],
            'Uttar Pradesh': [26.8467, 80.9462],
            'West Bengal': [22.9868, 87.8550],
            'Andhra Pradesh': [15.9129, 79.7400],
            'Telangana': [17.1232, 78.6569],
            'Madhya Pradesh': [22.9734, 78.6569],
            'Haryana': [29.0588, 76.0856],
            'Odisha': [20.9517, 85.0985]
        }
        return coordinates.get(state_name, [20.5937, 78.9629])  # Default to India center

def main():
    """Main function for command line execution"""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No data provided"}))
        return
    
    try:
        # Parse input data
        input_data = json.loads(sys.argv[1])
        
        # Initialize ML engine
        ml_engine = SmartLogisticsML()
        
        # Process data
        ml_engine.load_data(input_data)
        ml_engine.preprocess_data()
        analysis_results = ml_engine.run_ai_analysis()
        
        # Generate outputs
        alerts = ml_engine.generate_alerts()
        improvements = ml_engine.generate_improvements(alerts)
        dashboard_summary = ml_engine.get_dashboard_summary()
        map_data = ml_engine.get_map_data()
        
        # Prepare final results
        results = {
            'success': True,
            'analysis': analysis_results.to_dict('records'),
            'alerts': alerts,
            'improvements': improvements,
            'dashboard_summary': dashboard_summary,
            'map_data': map_data,
            'timestamp': datetime.now().isoformat()
        }
        
        print(json.dumps(results, default=str))
        
    except Exception as e:
        error_result = {
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }
        print(json.dumps(error_result))

if __name__ == "__main__":
    main()
