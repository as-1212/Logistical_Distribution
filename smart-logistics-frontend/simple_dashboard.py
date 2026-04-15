import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Set page configuration
st.set_page_config(
    page_title="Smart Logistics AI Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SAP-inspired CSS styling
def load_css():
    st.markdown("""
    <style>
        .main-header {
            background: linear-gradient(135deg, #0A6ED1 0%, #0852A0 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            box-shadow: 0 2px 10px rgba(10, 110, 209, 0.1);
        }
        
        .kpi-card {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            border-left: 4px solid #0A6ED1;
            margin-bottom: 1rem;
        }
        
        .kpi-value {
            font-size: 2rem;
            font-weight: bold;
            color: #0A6ED1;
            margin-bottom: 0.5rem;
        }
        
        .kpi-label {
            color: #6B7280;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .chart-container {
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
        }
        
        .insight-card {
            background: linear-gradient(135deg, #F3F4F6 0%, #E5E7EB 100%);
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #10B981;
            margin-bottom: 1rem;
        }
        
        .alert-high {
            border-left-color: #EF4444 !important;
        }
        
        .alert-medium {
            border-left-color: #F59E0B !important;
        }
        
        .alert-low {
            border-left-color: #10B981 !important;
        }
        
        .activity-feed {
            max-height: 400px;
            overflow-y: auto;
            background: white;
            border-radius: 10px;
            padding: 1rem;
        }
        
        .activity-item {
            padding: 0.75rem;
            border-bottom: 1px solid #E5E7EB;
            margin-bottom: 0.5rem;
        }
        
        .activity-item:last-child {
            border-bottom: none;
        }
        
        .filter-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            margin-bottom: 1.5rem;
        }
    </style>
    """, unsafe_allow_html=True)

# Generate sample logistics data
def generate_sample_data():
    states = [
        'Maharashtra', 'Gujarat', 'Karnataka', 'Tamil Nadu', 'Uttar Pradesh',
        'Rajasthan', 'Madhya Pradesh', 'West Bengal', 'Andhra Pradesh', 'Telangana',
        'Kerala', 'Punjab', 'Haryana', 'Delhi', 'Bihar', 'Odisha', 'Assam'
    ]
    
    products = ['Electronics', 'Textiles', 'Automotive', 'Pharmaceuticals', 'Food & Beverages', 'Chemicals']
    
    data = []
    for state in states:
        for product in products:
            units_sold = random.randint(500, 5000)
            supply_available = random.randint(300, 6000)
            revenue = units_sold * random.uniform(50, 500)
            demand_score = (units_sold / supply_available) * 100
            
            data.append({
                'State': state,
                'Product': product,
                'Units_Sold': units_sold,
                'Supply_Available': supply_available,
                'Revenue': revenue,
                'Demand_Score': min(demand_score, 150),  # Cap at 150
                'Date': datetime.now() - timedelta(days=random.randint(0, 30))
            })
    
    return pd.DataFrame(data)

# Calculate KPIs
def calculate_kpis(df):
    total_orders = df['Units_Sold'].sum()
    total_revenue = df['Revenue'].sum()
    active_alerts = len(df[df['Demand_Score'] > 120])
    supply_efficiency = (df['Supply_Available'].sum() / (df['Units_Sold'].sum() + df['Supply_Available'].sum())) * 100
    
    return {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'active_alerts': active_alerts,
        'supply_efficiency': supply_efficiency
    }

# Generate AI insights
def generate_ai_insights(df):
    insights = []
    
    # High demand states
    high_demand = df[df['Demand_Score'] > 120]['State'].value_counts().head(3)
    if not high_demand.empty:
        insights.append({
            'type': 'warning',
            'title': 'High Demand Alert',
            'description': f"States with critical demand: {', '.join(high_demand.index[:3])}",
            'priority': 'high'
        })
    
    # Overstock regions
    overstock = df[df['Demand_Score'] < 50]['State'].value_counts().head(3)
    if not overstock.empty:
        insights.append({
            'type': 'info',
            'title': 'Overstock Regions',
            'description': f"Excess inventory in: {', '.join(overstock.index[:3])}",
            'priority': 'medium'
        })
    
    # Redistribution suggestions
    if not high_demand.empty and not overstock.empty:
        insights.append({
            'type': 'success',
            'title': 'Redistribution Opportunity',
            'description': f"Consider moving stock from {overstock.index[0]} to {high_demand.index[0]}",
            'priority': 'low'
        })
    
    return insights

# Generate activity feed
def generate_activity_feed():
    activities = [
        {'icon': '🚨', 'type': 'alert', 'title': 'Critical Shortage', 'description': 'Electronics in Maharashtra', 'priority': 'high'},
        {'icon': '📦', 'type': 'stock', 'title': 'New Shipment', 'description': '500 units arrived at Delhi warehouse', 'priority': 'low'},
        {'icon': '🤖', 'type': 'ai', 'title': 'AI Recommendation', 'description': 'Increase supply for Tamil Nadu by 20%', 'priority': 'medium'},
        {'icon': '📈', 'type': 'performance', 'title': 'Efficiency Improved', 'description': 'Supply chain efficiency up 5%', 'priority': 'low'},
        {'icon': '🚚', 'type': 'logistics', 'title': 'Route Optimized', 'description': 'Mumbai-Pune route time reduced by 15%', 'priority': 'medium'},
    ]
    
    # Add timestamps
    for activity in activities:
        activity['timestamp'] = datetime.now() - timedelta(minutes=random.randint(1, 60))
    
    return activities

# Create India map data
def create_india_map_data(df):
    # Simplified state coordinates for demonstration
    state_coords = {
        'Maharashtra': [19.0760, 72.8777],
        'Gujarat': [23.2156, 72.6369],
        'Karnataka': [12.9716, 77.5946],
        'Tamil Nadu': [11.1271, 78.6569],
        'Uttar Pradesh': [26.8467, 80.9462],
        'Rajasthan': [26.9124, 75.7873],
        'Madhya Pradesh': [22.9734, 78.6569],
        'West Bengal': [22.9868, 87.8550],
        'Andhra Pradesh': [15.9129, 79.7400],
        'Telangana': [17.3850, 78.4867],
        'Kerala': [10.8505, 76.2711],
        'Punjab': [31.1471, 75.3412],
        'Haryana': [29.0588, 76.0856],
        'Delhi': [28.7041, 77.1025],
        'Bihar': [25.0961, 85.3131],
        'Odisha': [20.9517, 85.0985],
        'Assam': [26.2006, 92.9376]
    }
    
    map_data = df.groupby('State')['Demand_Score'].mean().reset_index()
    map_data['lat'] = map_data['State'].map(lambda x: state_coords.get(x, [20, 77])[0])
    map_data['lon'] = map_data['State'].map(lambda x: state_coords.get(x, [20, 77])[1])
    
    return map_data

# Main dashboard
def main():
    load_css()
    
    # Generate data
    df = generate_sample_data()
    kpis = calculate_kpis(df)
    insights = generate_ai_insights(df)
    activities = generate_activity_feed()
    map_data = create_india_map_data(df)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🚚 Smart Logistics AI Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Real-time Supply Chain Intelligence & Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['total_orders']:,}</div>
            <div class="kpi-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">₹{kpis['total_revenue']:,.0f}</div>
            <div class="kpi-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        alert_class = "alert-high" if kpis['active_alerts'] > 5 else "alert-medium" if kpis['active_alerts'] > 2 else "alert-low"
        st.markdown(f"""
        <div class="kpi-card {alert_class}">
            <div class="kpi-value">{kpis['active_alerts']}</div>
            <div class="kpi-label">Active Alerts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['supply_efficiency']:.1f}%</div>
            <div class="kpi-label">Supply Efficiency</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter Bar
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_product = st.selectbox('Product', ['All'] + list(df['Product'].unique()))
    
    with col2:
        selected_state = st.selectbox('State', ['All'] + list(df['State'].unique()))
    
    with col3:
        date_range = st.date_input(
            'Date Range',
            value=[datetime.now() - timedelta(days=7), datetime.now()],
            max_value=datetime.now()
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    if selected_product != 'All':
        filtered_df = filtered_df[filtered_df['Product'] == selected_product]
    if selected_state != 'All':
        filtered_df = filtered_df[filtered_df['State'] == selected_state]
    
    # Main Grid (2x2 Layout)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📊 Total Orders by Month")
        
        # Monthly orders data
        monthly_orders = filtered_df.groupby(filtered_df['Date'].dt.strftime('%Y-%m'))['Units_Sold'].sum().reset_index()
        monthly_orders.columns = ['Month', 'Orders']
        
        fig_orders = go.Figure(data=[go.Bar(x=monthly_orders['Month'], y=monthly_orders['Orders'], marker_color='#0A6ED1')])
        fig_orders.update_layout(template='plotly_white', height=300, margin=dict(l=20, r=20, t=40, b=20))
        
        st.plotly_chart(fig_orders, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Revenue Trend
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💰 Revenue Trend")
        
        monthly_revenue = filtered_df.groupby(filtered_df['Date'].dt.strftime('%Y-%m'))['Revenue'].sum().reset_index()
        monthly_revenue.columns = ['Month', 'Revenue']
        
        fig_revenue = go.Figure(data=[go.Scatter(x=monthly_revenue['Month'], y=monthly_revenue['Revenue'], line=dict(color='#10B981'))])
        fig_revenue.update_layout(template='plotly_white', height=300, margin=dict(l=20, r=20, t=40, b=20))
        
        st.plotly_chart(fig_revenue, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        # Distribution Pie Chart
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🥧 Distribution by Product")
        
        product_dist = filtered_df.groupby('Product')['Units_Sold'].sum().reset_index()
        
        fig_pie = px.pie(
            product_dist,
            values='Units_Sold',
            names='Product',
            template='plotly_white',
            color_discrete_sequence=['#0A6ED1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
        )
        
        fig_pie.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        
        st.plotly_chart(fig_pie, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Demand Heatmap
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🔥 Demand Heatmap (State vs Product)")
        
        heatmap_data = filtered_df.pivot_table(
            values='Demand_Score',
            index='State',
            columns='Product',
            aggfunc='mean'
        ).fillna(0)
        
        fig_heatmap = px.imshow(
            heatmap_data,
            template='plotly_white',
            color_continuous_scale='RdYlBu_r',
            aspect='auto'
        )
        
        fig_heatmap.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # India Map Section
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🗺️ India Demand Distribution")
    
    fig_map = px.scatter_mapbox(
        map_data,
        lat='lat',
        lon='lon',
        size='Demand_Score',
        color='Demand_Score',
        hover_name='State',
        color_continuous_scale=['#10B981', '#F59E0B', '#EF4444', '#0A6ED1'],
        size_max=50,
        zoom=4,
        center={'lat': 20, 'lon': 77},
        mapbox_style='open-street-map',
        template='plotly_white'
    )
    
    fig_map.update_layout(height=400, margin=dict(l=20, r=20, t=40, b=20))
    
    st.plotly_chart(fig_map, use_container_width=True)
    
    # Demand Score Legend
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #10B981; border-radius: 50%;"></div>
            <span>Balanced (0-50)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #F59E0B; border-radius: 50%;"></div>
            <span>Moderate (50-80)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #EF4444; border-radius: 50%;"></div>
            <span>High Demand (80-120)</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #0A6ED1; border-radius: 50%;"></div>
            <span>Excess (>120)</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Insights and Activity Feed
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("🤖 AI Insights")
        
        for insight in insights:
            alert_class = f"alert-{insight['priority']}"
            st.markdown(f"""
            <div class="insight-card {alert_class}">
                <h4 style="margin: 0 0 0.5rem 0; color: #1F2937;">{insight['title']}</h4>
                <p style="margin: 0; color: #6B7280;">{insight['description']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("📡 Live Activity Feed")
        
        st.markdown('<div class="activity-feed">', unsafe_allow_html=True)
        
        icon_color = {
            'alert': '#EF4444',
            'stock': '#10B981',
            'ai': '#0A6ED1',
            'performance': '#F59E0B',
            'logistics': '#8B5CF6'
        }
        
        for activity in activities:
            time_ago = (datetime.now() - activity['timestamp']).seconds // 60
            
            st.markdown(f"""
            <div class="activity-item">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{activity['icon']}</span>
                    <div>
                        <strong style="color: {icon_color[activity['type']]};">{activity['title']}</strong>
                        <br>
                        <small style="color: #6B7280;">{activity['description']}</small>
                        <br>
                        <small style="color: #9CA3AF;">{time_ago} min ago</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Export Button
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div style="padding: 1rem; background: #F9FAFB; border-radius: 8px;">
            <h4 style="margin: 0 0 0.5rem 0; color: #1F2937;">📊 Dashboard Summary</h4>
            <p style="margin: 0; color: #6B7280; font-size: 0.9rem;">
                Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | 
                Data Points: {len(filtered_df)} records | 
                Refresh Rate: Manual | 
                Status: 🟢 Live
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("📥 Export to CSV", type="primary"):
            csv_data = filtered_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv_data,
                file_name=f"logistics_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Manual refresh
    if st.button("🔄 Refresh Now", type="secondary"):
        st.rerun()

if __name__ == "__main__":
    main()
