import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
from dateutil.relativedelta import relativedelta
from map_utils import create_india_map, INDIA_STATE_COORDINATES

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
            color: #EF4444;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: bold;
        }
        
        .kpi-percentage {
            color: #FCD34D;
            font-size: 1.2rem;
            font-weight: bold;
            margin-top: 0.5rem;
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
            background: linear-gradient(135deg, #064E3B 0%, #0D7D5A 100%);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(13, 125, 90, 0.1);
            margin-bottom: 1.5rem;
            margin-top: 0.25rem;
            border: 1px solid #0D7D5A;
        }
        
        .filter-label {
            color: #FFFFFF;
            font-weight: bold;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .stSelectbox > div > div {
            background-color: #0D7D5A;
            color: #FFFFFF;
            border: 1px solid #064E3B;
        }
        
        .stDateInput > div > div {
            background-color: #0D7D5A;
            color: #FFFFFF;
            border: 1px solid #064E3B;
        }
        
        .stSelectbox > div > div > div {
            background-color: white;
        }
        
        .stDateInput > div > div > div {
            background-color: white;
        }
        
        .metric-container {
            background: white;
            padding: 1rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: bold;
            color: #0A6ED1;
        }
        
        .metric-label {
            font-size: 0.8rem;
            color: #6B7280;
            margin-top: 0.25rem;
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
    # Use coordinates from map_utils for accuracy
    map_data = df.groupby('State')['Demand_Score'].mean().reset_index()
    map_data['lat'] = map_data['State'].map(lambda x: INDIA_STATE_COORDINATES.get(x, [20, 77])[0])
    map_data['lon'] = map_data['State'].map(lambda x: INDIA_STATE_COORDINATES.get(x, [20, 77])[1])
    
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
            <div class="kpi-percentage">+12.5%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">₹{kpis['total_revenue']:,.0f}</div>
            <div class="kpi-label">Total Revenue</div>
            <div class="kpi-percentage">+8.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['active_alerts']}</div>
            <div class="kpi-label">AI Predictions</div>
            <div class="kpi-percentage">+15% forecast</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['supply_efficiency']:.1f}%</div>
            <div class="kpi-label">Efficiency</div>
            <div class="kpi-percentage">+3.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Filter Bar
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="filter-label">Product</div>', unsafe_allow_html=True)
        selected_product = st.selectbox('Product', ['All'] + list(df['Product'].unique()), label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="filter-label">State</div>', unsafe_allow_html=True)
        selected_state = st.selectbox('State', ['All'] + list(df['State'].unique()), label_visibility="collapsed")
    
    with col3:
        st.markdown('<div class="filter-label">Date Range</div>', unsafe_allow_html=True)
        date_range = st.date_input(
            'Date Range',
            value=[datetime.now() - timedelta(days=7), datetime.now()],
            max_value=datetime.now(),
            label_visibility="collapsed"
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
        
        fig_orders = px.bar(
            monthly_orders,
            x='Month',
            y='Orders',
            template='plotly_white',
            color_discrete_map={'Orders': '#0A6ED1'}
        )
        
        fig_orders.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_orders, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Revenue Trend
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.subheader("💰 Revenue Trend")
        
        monthly_revenue = filtered_df.groupby(filtered_df['Date'].dt.strftime('%Y-%m'))['Revenue'].sum().reset_index()
        monthly_revenue.columns = ['Month', 'Revenue']
        
        fig_revenue = px.line(
            monthly_revenue,
            x='Month',
            y='Revenue',
            template='plotly_white',
            color_discrete_map={'Revenue': '#10B981'}
        )
        
        fig_revenue.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_revenue, width='stretch')
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
        
        fig_pie.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_pie, width='stretch')
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
        
        fig_heatmap.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=40, b=20),
            paper_bgcolor='white'
        )
        
        st.plotly_chart(fig_heatmap, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # India Map Section
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🗺️ India Demand Distribution")
    
    # Use improved map visualization
    fig_map = create_india_map(map_data, title="Regional Demand Score Analysis")
    st.plotly_chart(fig_map, width='stretch')
    
    # Demand Score Legend
    st.markdown("""
    <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 1rem; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #EF4444; border-radius: 50%; border: 2px solid white;"></div>
            <span><b>Critical (>3.5)</b></span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #F97316; border-radius: 50%; border: 2px solid white;"></div>
            <span><b>High (2.5-3.5)</b></span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #F59E0B; border-radius: 50%; border: 2px solid white;"></div>
            <span><b>Moderate (1.5-2.5)</b></span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #60A5FA; border-radius: 50%; border: 2px solid white;"></div>
            <span><b>Low (0.5-1.5)</b></span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.5rem;">
            <div style="width: 20px; height: 20px; background: #D1D5DB; border-radius: 50%; border: 2px solid white;"></div>
            <span><b>None (<0.5)</b></span>
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
                Refresh Rate: 5 seconds | 
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
    
    # Auto-refresh
    if st.button("🔄 Refresh Now", type="secondary"):
        st.rerun()

if __name__ == "__main__":
    main()
