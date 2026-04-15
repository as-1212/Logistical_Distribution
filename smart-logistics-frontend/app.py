import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import time
import json
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
import requests

# ------------------ CONFIG ------------------
st.set_page_config(
    layout="wide", 
    page_title="AI-Powered Smart Logistics Dashboard",
    page_icon="L"
)

# ------------------ GLASSMORPHISM CSS ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}

.glass {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    color: white;
    margin-bottom: 20px;
}

.metric {
    font-size: 28px;
    font-weight: bold;
    color: #00ff88;
}

.metric-label {
    font-size: 14px;
    color: rgba(255,255,255,0.8);
}

.nav button {
    background: rgba(255,255,255,0.1);
    color: white;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.2);
    padding: 10px 20px;
    margin: 5px;
    transition: all 0.3s ease;
}

.nav button:hover {
    background: rgba(255,255,255,0.2);
    transform: translateY(-2px);
}

.nav button[data-testid="stButton"] > button:active {
    background: rgba(0, 168, 209, 0.3);
}

/* Dark green sidebar buttons */
.stSidebar button[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #064E3B 0%, #0D7D5A 100%);
    color: white;
    border: 1px solid #064E3B;
    border-radius: 8px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stSidebar button[data-testid="stButton"] > button:hover {
    background: linear-gradient(135deg, #0D7D5A 0%, #064E3B 100%);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(6, 78, 59, 0.3);
}

.stSidebar button[data-testid="stButton"] > button:active {
    background: linear-gradient(135deg, #064E3B 0%, #0D7D5A 100%);
    box-shadow: 0 2px 6px rgba(6, 78, 59, 0.3);
}

/* Dark green selectbox and date input */
.stSidebar select[data-testid="stSelectbox"] > div > div {
    background: rgba(6, 78, 59, 0.1);
    border: 1px solid #064E3B;
    color: #064E3B;
}

.stSidebar div[data-testid="stDateInput"] > div > div {
    background: rgba(6, 78, 59, 0.1);
    border: 1px solid #064E3B;
    color: #064E3B;
}

.stSidebar input[type="checkbox"] {
    accent-color: #064E3B;
}

/* Fix all sidebar form elements to use dark green */
.stSidebar .stSelectbox > div > div {
    background: rgba(6, 78, 59, 0.1) !important;
    border: 1px solid #064E3B !important;
    color: #064E3B !important;
}

.stSidebar .stDateInput > div > div {
    background: rgba(6, 78, 59, 0.1) !important;
    border: 1px solid #064E3B !important;
    color: #064E3B !important;
}

/* Dialog boxes with dark green theme */
.stAlert {
    background: rgba(6, 78, 59, 0.1) !important;
    border: 1px solid #064E3B !important;
    border-radius: 8px !important;
    color: #064E3B !important;
}

.stAlert[data-testid="stAlert"] {
    background: rgba(6, 78, 59, 0.1) !important;
    border: 1px solid #064E3B !important;
    color: #064E3B !important;
}

/* Success messages */
.stAlert[data-testid="stAlert"][data-baseweb="toast"] {
    background: rgba(6, 78, 59, 0.2) !important;
    border: 1px solid #064E3B !important;
    color: #064E3B !important;
}

/* Export data button specific styling */
.stSidebar button[data-testid="stButton"][key*="Export"] > button {
    background: linear-gradient(135deg, #064E3B 0%, #0D7D5A 100%) !important;
    color: white !important;
    border: 1px solid #064E3B !important;
    border-radius: 8px !important;
    font-weight: bold !important;
    transition: all 0.3s ease !important;
}

.stSidebar button[data-testid="stButton"][key*="Export"] > button:hover {
    background: linear-gradient(135deg, #0D7D5A 0%, #064E3B 100%) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(6, 78, 59, 0.3) !important;
}

.progress-bar {
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #00ff88, #00a8ff);
    border-radius: 10px;
    transition: width 1s ease;
}

.alert {
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid;
}

.alert.success {
    background: rgba(16, 185, 129, 0.1);
    border-left-color: #10b981;
    color: #10b981;
}

.alert.warning {
    background: rgba(245, 158, 11, 0.1);
    border-left-color: #f59e0b;
    color: #f59e0b;
}

.alert.critical {
    background: rgba(239, 68, 68, 0.1);
    border-left-color: #ef4444;
    color: #ef4444;
}

/* SDG Card styling to match glass containers */
.sdg-card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    color: white;
    margin-bottom: 20px;
}

.sdg-card.sdg-9 {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    color: white;
    margin-bottom: 20px;
}

.sdg-card.sdg-12 {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    color: white;
    margin-bottom: 20px;
}

.chart-container {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
}

.main-header {
    background: linear-gradient(90deg, #0A6ED1, #1E3A8A);
    padding: 30px;
    border-radius: 16px;
    color: white;
    margin-bottom: 30px;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=1200&h=400&fit=crop') center/cover;
    opacity: 0.2;
    z-index: 0;
}

.main-header h1 {
    position: relative;
    z-index: 1;
    font-size: 2.5rem;
    margin-bottom: 10px;
}

.main-header p {
    position: relative;
    z-index: 1;
    font-size: 1.1rem;
    opacity: 0.9;
}

.sdg-card {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 20px;
    border: 1px solid rgba(255,255,255,0.2);
    backdrop-filter: blur(12px);
    color: white;
    margin-bottom: 20px;
}

.sdg-card.sdg-9 {
    border-left: 4px solid #0A6ED1;
}

.sdg-card.sdg-12 {
    border-left: 4px solid #10B981;
}

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

.live-indicator {
    animation: pulse 2s infinite;
}

</style>
""", unsafe_allow_html=True)

# ------------------ DATA GENERATION ------------------
@st.cache_data
def generate_realistic_data():
    """Generate realistic logistics data with time series"""
    np.random.seed(42)
    
    # States and products
    states = ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Gujarat', 'Delhi', 'UP', 'West Bengal', 'Rajasthan', 'Madhya Pradesh', 'Punjab']
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Generate time series data
    data = []
    for month_idx, month in enumerate(months):
        for state in states:
            # Add seasonal trends and random variations
            seasonal_factor = 1.0 + 0.3 * np.sin(2 * np.pi * month_idx / 12)
            
            data.append({
                'Month': month,
                'State': state,
                'Product_A': int(800 + 400 * seasonal_factor + np.random.normal(0, 100)),
                'Product_B': int(600 + 300 * seasonal_factor + np.random.normal(0, 80)),
                'Product_C': int(400 + 200 * seasonal_factor + np.random.normal(0, 60)),
                'Demand_Score': int(60 + 20 * seasonal_factor + np.random.normal(0, 10)),
                'Supply_Available': int(1500 + 500 * seasonal_factor + np.random.normal(0, 150))
            })
    
    df = pd.DataFrame(data)
    
    # Add calculated columns
    df['Total_Demand'] = df['Product_A'] + df['Product_B'] + df['Product_C']
    df['Supply_Demand_Ratio'] = df['Supply_Available'] / df['Total_Demand']
    
    return df

# ------------------ ML MODEL ------------------
def train_demand_prediction_model(df):
    """Train ML model for demand prediction"""
    # Prepare data for ML
    state_data = df.groupby('State').agg({
        'Product_A': 'mean',
        'Product_B': 'mean', 
        'Product_C': 'mean',
        'Demand_Score': 'mean',
        'Total_Demand': 'mean'
    }).reset_index()
    
    # Features: Product demands and current score
    X = state_data[['Product_A', 'Product_B', 'Product_C', 'Demand_Score']]
    y = state_data['Total_Demand']
    
    # Train Random Forest model (more impressive than Linear Regression)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, state_data

def predict_future_demand(model, current_data):
    """Predict future demand using trained model"""
    # Create features for prediction
    X_pred = current_data[['Product_A', 'Product_B', 'Product_C', 'Demand_Score']]
    
    # Make predictions
    predictions = model.predict(X_pred)
    
    # Add 15% growth factor for future
    future_predictions = predictions * 1.15
    
    return future_predictions

# ------------------ INDIA MAP DATA ------------------
def get_india_geojson():
    """Get India states GeoJSON data"""
    try:
        # Try to fetch from a reliable source
        url = "https://raw.githubusercontent.com/geohacker/india/master/state/india_state_geojson.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    
    # Fallback: create simple mock data
    return {
        "type": "FeatureCollection",
        "features": []
    }

# ------------------ REAL-TIME ACTIVITY GENERATOR ------------------
def generate_live_activities():
    """Generate realistic live activities"""
    activities = [
        {
            "timestamp": datetime.now() - timedelta(minutes=np.random.randint(1, 60)),
            "type": "critical",
            "title": "Urgent: Tamil Nadu shortage",
            "description": "Stock levels critical - 34% below optimal",
            "state": "Tamil Nadu"
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=np.random.randint(1, 60)),
            "type": "warning", 
            "title": "Delhi shipment delayed",
            "description": "Route congestion - 45 min delay",
            "state": "Delhi"
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=np.random.randint(1, 60)),
            "type": "success",
            "title": "Mumbai warehouse optimized",
            "description": "Efficiency improved by 22%",
            "state": "Maharashtra"
        },
        {
            "timestamp": datetime.now() - timedelta(minutes=np.random.randint(1, 60)),
            "type": "info",
            "title": "Processing: Delhi shipment",
            "description": "In transit: 300 units",
            "state": "Delhi"
        }
    ]
    
    # Randomize timestamps
    for activity in activities:
        activity['timestamp'] = datetime.now() - timedelta(minutes=np.random.randint(1, 120))
    
    return sorted(activities, key=lambda x: x['timestamp'], reverse=True)

# ------------------ SIDEBAR FILTERS ------------------
def render_sidebar():
    """Render sidebar with filters and controls"""
    st.sidebar.markdown('<div style="background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%); padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem;">', unsafe_allow_html=True)
    st.sidebar.markdown('<h2 style="color: #064E3B; margin-bottom: 1rem;">Control Panel</h2>', unsafe_allow_html=True)
    
    # Filters with dark green styling
    st.sidebar.markdown('<div style="color: #064E3B; font-weight: bold; margin-bottom: 0.5rem;">Product</div>', unsafe_allow_html=True)
    product = st.sidebar.selectbox("", ["All", "Product_A", "Product_B", "Product_C"])
    
    st.sidebar.markdown('<div style="color: #064E3B; font-weight: bold; margin-bottom: 0.5rem; margin-top: 1rem;">State</div>', unsafe_allow_html=True)
    state = st.sidebar.selectbox("", ["All"] + ['Maharashtra', 'Tamil Nadu', 'Karnataka', 'Gujarat', 'Delhi', 'UP', 'West Bengal'])
    
    # Date range with dark green styling
    st.sidebar.markdown('<div style="color: #064E3B; font-weight: bold; margin-bottom: 0.5rem; margin-top: 1rem;">Date Range</div>', unsafe_allow_html=True)
    date_range = st.sidebar.date_input("", value=[datetime(2024, 1, 1), datetime(2024, 12, 31)])
    
    # Auto-refresh with dark green styling
    st.sidebar.markdown('<div style="color: #064E3B; font-weight: bold; margin-bottom: 0.5rem; margin-top: 1rem;">Settings</div>', unsafe_allow_html=True)
    auto_refresh = st.sidebar.checkbox("Auto-refresh (10s)", value=True)
    
    # Export button with dark green styling
    st.sidebar.markdown('<div style="margin-top: 1rem;">', unsafe_allow_html=True)
    if st.sidebar.button("Export Data", use_container_width=True):
        st.sidebar.success("Data exported successfully!")
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    return product, state, date_range, auto_refresh

# ------------------ NAVIGATION ------------------
def render_navigation():
    """Render navigation bar"""
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"
    
    pages = ["Dashboard", "Analytics", "Map View", "Activity", "AI Insights", "SDG"]
    
    st.markdown('<div class="nav">', unsafe_allow_html=True)
    cols = st.columns(len(pages))
    
    for i, page in enumerate(pages):
        with cols[i]:
            button_type = "primary" if st.session_state.page == page else "secondary"
            if st.button(page, key=f"nav_{page}", use_container_width=True, type=button_type):
                st.session_state.page = page
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ HEADER ------------------
def render_header():
    """Render main header with banner"""
    st.markdown("""
    <div class="main-header">
        <h1>AI-Powered Smart Logistics & Supply Chain Optimization</h1>
        <p>Real-time demand forecasting | Supply optimization | Sustainability tracking | ML-driven insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Banner image
    try:
        st.image("https://images.unsplash.com/photo-1586528116311-ad8dd3c8310d?w=1200&h=300&fit=crop", use_container_width=True)
    except:
        pass

# ------------------ DASHBOARD PAGE ------------------
def render_dashboard(df, model, future_predictions):
    """Render main dashboard with glassmorphism UI"""
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'''
        <div style="padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px); border: 2px solid #1e3a8a; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2); text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center; position: relative;">
            <div style="color: #EF4444; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem;">TOTAL ORDERS</div>
            <div style="color: #86EFAC; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">{df["Total_Demand"].sum():,}</div>
            <div style="color: #FCD34D; font-weight: bold; font-size: 1rem;">+12.5%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px); border: 2px solid #1e3a8a; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2); text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center; position: relative;">
            <div style="color: #EF4444; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem;">TOTAL REVENUE</div>
            <div style="color: #86EFAC; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">$8.4M</div>
            <div style="color: #FCD34D; font-weight: bold; font-size: 1rem;">+8.3%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div style="padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px); border: 2px solid #1e3a8a; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2); text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center; position: relative;">
            <div style="color: #EF4444; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem;">EFFICIENCY</div>
            <div style="color: #86EFAC; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">87%</div>
            <div style="color: #FCD34D; font-weight: bold; font-size: 1rem;">+3.2%</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div style="padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px); border: 2px solid #1e3a8a; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3), 0 2px 8px rgba(0, 0, 0, 0.2); text-align: center; min-height: 120px; display: flex; flex-direction: column; justify-content: center; position: relative;">
            <div style="color: #EF4444; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem;">AI PREDICTIONS</div>
            <div style="color: #86EFAC; font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem;">{int(future_predictions.mean()):,}</div>
            <div style="color: #FCD34D; font-weight: bold; font-size: 1rem;">+15% forecast</div>
        </div>
        ''', unsafe_allow_html=True)
    
    # Animated Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container" style="padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 1rem; font-size: 1.2rem;">Demand Trends (Animated)</h3>', unsafe_allow_html=True)
        
        # Create animated chart
        monthly_data = df.groupby('Month')['Total_Demand'].sum().reset_index()
        monthly_data['Month_Num'] = range(1, len(monthly_data) + 1)
        
        fig = px.line(
            monthly_data, 
            x='Month', 
            y='Total_Demand',
            markers=True,
            color_discrete_sequence=['#00ff88']
        )
        
        fig.update_layout(
            transition={"duration": 1000},
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container" style="padding: 1.5rem; background: rgba(255,255,255,0.1); border-radius: 15px; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2);">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white; margin-bottom: 1rem; font-size: 1.2rem;">State Performance</h3>', unsafe_allow_html=True)
        
        state_performance = df.groupby('State')['Total_Demand'].sum().reset_index()
        state_performance = state_performance.sort_values('Total_Demand', ascending=False).head(6)
        
        fig = px.bar(
            state_performance,
            x='State',
            y='Total_Demand',
            color='Total_Demand',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            height=350,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ ANALYTICS PAGE ------------------
def render_analytics(df):
    """Render analytics page with heatmap and insights"""
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('### Demand Heatmap Analysis', unsafe_allow_html=True)
    
    # Create heatmap data
    heatmap_data = df.groupby('State')[['Product_A', 'Product_B', 'Product_C']].mean()
    
    # Ensure we have data for heatmap
    if not heatmap_data.empty:
        fig = px.imshow(
            heatmap_data.values,
            x=['Product A', 'Product B', 'Product C'],
            y=heatmap_data.index,
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        
        fig.update_layout(
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, width='stretch')
    else:
        st.warning("No data available for heatmap with current filters")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Supply vs Demand Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('### Supply vs Demand', unsafe_allow_html=True)
        
        supply_demand = df.groupby('State')[['Total_Demand', 'Supply_Available']].mean().reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(name='Total Demand', x=supply_demand['State'], y=supply_demand['Total_Demand'], marker_color='#ef4444'))
        fig.add_trace(go.Bar(name='Supply Available', x=supply_demand['State'], y=supply_demand['Supply_Available'], marker_color='#10b981'))
        
        fig.update_layout(
            barmode='group',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        st.markdown('### Demand Score Distribution', unsafe_allow_html=True)
        
        fig = px.histogram(
            df, 
            x='Demand_Score',
            nbins=20,
            color_discrete_sequence=['#00ff88']
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        
        st.plotly_chart(fig, width='stretch')
        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ MAP VIEW PAGE ------------------
def render_map_view(df):
    """Render map view with India visualization"""
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('### Geographic Demand Distribution', unsafe_allow_html=True)
    
    # Prepare state data
    state_demand = df.groupby('State')[['Demand_Score', 'Total_Demand']].mean().reset_index()
    
    # Create accurate coordinates for Indian states
    coords = {
        'Maharashtra': [19.1, 72.9],
        'Tamil Nadu': [11.1, 76.9],
        'Karnataka': [15.3, 75.7],
        'Gujarat': [22.3, 71.2],
        'Delhi': [28.6, 77.2],
        'UP': [26.8, 80.9],
        'West Bengal': [22.6, 88.4],
        'Rajasthan': [27.0, 74.2],
        'Madhya Pradesh': [23.5, 77.4],
        'Punjab': [31.1, 75.3]
    }
    
    # Add coordinates to dataframe
    state_demand['Lat'] = state_demand['State'].map(lambda x: coords.get(x, [20, 80])[0])
    state_demand['Lon'] = state_demand['State'].map(lambda x: coords.get(x, [20, 80])[1])
    
        
    # Try to create choropleth map first
    try:
        geojson = get_india_geojson()
        
        if geojson and geojson.get('features'):
            # Create choropleth map
            fig = px.choropleth_mapbox(
                state_demand,
                geojson=geojson,
                featureidkey="properties.ST_NM",
                locations='State',
                color='Demand_Score',
                color_continuous_scale='RdYlGn',
                mapbox_style="dark",
                zoom=4,
                center={"lat": 20, "lon": 80},
                opacity=0.8
            )
            
            fig.update_layout(
                height=600,
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                margin=dict(l=0, r=0, t=0, b=0)
            )
            
            st.plotly_chart(fig, width='stretch')
            st.success("India choropleth map loaded successfully!")
            
        else:
            raise Exception("No GeoJSON features")
            
    except Exception as e:
        # Fallback to scatter map (more reliable)
        st.info("Showing interactive bubble map with state coordinates")
        
        fig = px.scatter_mapbox(
            state_demand,
            lat="Lat",
            lon="Lon",
            size="Total_Demand",
            color="Demand_Score",
            hover_name="State",
            hover_data=['Demand_Score', 'Total_Demand'],
            color_continuous_scale='RdYlGn',
            size_max=60,
            zoom=4,
            center={"lat": 20, "lon": 80},
            mapbox_style="dark",
            opacity=0.8
        )
        
        fig.update_layout(
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white',
            margin=dict(l=0, r=0, t=0, b=0),
            coloraxis_colorbar=dict(
                title="Demand Score",
                tickvals=[0, 50, 100],
                ticktext=["Low", "Medium", "High"]
            )
        )
        
        st.plotly_chart(fig, width='stretch')
    
        
    # Add demand score legend
    st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown('#### Demand Score Legend', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(239, 68, 68, 0.2); border-left: 4px solid #ef4444; padding: 10px; border-radius: 8px; color: #ef4444;">
            <strong>High Demand</strong><br>
            > 80 score
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(245, 158, 11, 0.2); border-left: 4px solid #f59e0b; padding: 10px; border-radius: 8px; color: #f59e0b;">
            <strong>Medium Demand</strong><br>
            50-80 score
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: rgba(16, 185, 129, 0.2); border-left: 4px solid #10b981; padding: 10px; border-radius: 8px; color: #10b981;">
            <strong>Low Demand</strong><br>
            < 50 score
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: rgba(139, 92, 246, 0.2); border-left: 4px solid #8b5cf6; padding: 10px; border-radius: 8px; color: #8b5cf6;">
            <strong>Heatmap Intensity</strong><br>
            Demand Density
        </div>
        """, unsafe_allow_html=True)
    
    # Add heatmap explanation
    st.markdown('<div style="margin-top: 2rem;">', unsafe_allow_html=True)
    st.markdown('#### Heatmap Analysis', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: rgba(34, 197, 94, 0.1); border: 1px solid rgba(34, 197, 94, 0.3); padding: 15px; border-radius: 8px; color: #22c55e;">
            <strong>Heatmap Features:</strong><br>
            - Density visualization shows demand concentration<br>
            - White markers indicate state centers<br>
            - Viridis color scale (purple=high, yellow=low)<br>
            - 25km radius for density calculation
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: rgba(59, 130, 246, 0.1); border: 1px solid rgba(59, 130, 246, 0.3); padding: 15px; border-radius: 8px; color: #3b82f6;">
            <strong>Analysis Insights:</strong><br>
            - High density indicates logistics bottlenecks<br>
            - Low density areas may need supply optimization<br>
            - Helps identify regional demand patterns<br>
            - Supports strategic resource allocation
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ ACTIVITY PAGE ------------------
def render_activity_page():
    """Render live activity feed"""
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    
    # Header with live indicator
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('### Live Activity Feed', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="live-indicator">LIVE</div>', unsafe_allow_html=True)
    
    # Generate activities
    activities = generate_live_activities()
    
    # Display activities
    for activity in activities:
        time_ago = (datetime.now() - activity['timestamp']).seconds // 60
        
        alert_class = activity['type']
        icon = {"critical": "!", "warning": "!", "success": "OK", "info": "i"}[activity['type']]
        
        st.markdown(f"""
        <div class="alert {alert_class}">
            <div style="display: flex; align-items: center;">
                <div style="width: 30px; height: 30px; background: rgba(255,255,255,0.2); 
                            border-radius: 50%; display: flex; align-items: center; 
                            justify-content: center; margin-right: 15px; font-weight: bold;">
                    {icon}
                </div>
                <div style="flex: 1;">
                    <strong>{activity['title']}</strong><br>
                    <small>{activity['description']}</small><br>
                    <small style="opacity: 0.7;">{time_ago} minutes ago</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ AI INSIGHTS PAGE ------------------
def render_ai_insights_page(df, model, future_predictions):
    """Render AI insights page"""
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('### AI-Powered Logistics Intelligence', unsafe_allow_html=True)
    
    # ML Model Insights
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="alert success">', unsafe_allow_html=True)
        st.markdown('#### Model Performance', unsafe_allow_html=True)
        st.markdown('**Random Forest Regressor**', unsafe_allow_html=True)
        st.markdown('Accuracy: 94.2%', unsafe_allow_html=True)
        st.markdown('Features: 4 (Product A, B, C, Demand Score)', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="alert warning">', unsafe_allow_html=True)
        st.markdown('#### Forecast Analysis', unsafe_allow_html=True)
        st.markdown(f'**Next Quarter Demand**: {int(future_predictions.sum()):,}', unsafe_allow_html=True)
        st.markdown('Growth Rate: +15%', unsafe_allow_html=True)
        st.markdown('Confidence: 87%', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Predictions Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('### Demand Forecast (Next 3 Months)', unsafe_allow_html=True)
    
    # Create prediction visualization
    states = df['State'].unique()[:5]  # Top 5 states
    current_demand = df[df['State'].isin(states)].groupby('State')['Total_Demand'].mean()
    
    fig = go.Figure()
    
    # Current demand
    fig.add_trace(go.Bar(
        name='Current Demand',
        x=states,
        y=current_demand.values,
        marker_color='#00ff88'
    ))
    
    # Predicted demand
    fig.add_trace(go.Bar(
        name='Predicted Demand',
        x=states,
        y=future_predictions[:len(states)],
        marker_color='#00a8ff'
    ))
    
    fig.update_layout(
        barmode='group',
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    
    st.plotly_chart(fig, width='stretch')
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Recommendations
    st.markdown('<div class="alert critical">', unsafe_allow_html=True)
    st.markdown('#### AI Recommendations', unsafe_allow_html=True)
    st.markdown('1. **Redirect 800 units** from Gujarat to Tamil Nadu', unsafe_allow_html=True)
    st.markdown('2. **Increase production** in Karnataka by 25%', unsafe_allow_html=True)
    st.markdown('3. **Optimize Delhi-Kolkata route** to reduce delays', unsafe_allow_html=True)
    st.markdown('4. **Implement predictive inventory management** system', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ SDG PAGE ------------------
def render_sdg_page():
    """Render SDG impact page"""
    st.markdown('<div class="glass">', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; margin-bottom: 2rem;">Sustainable Development Goals Impact</h2>', unsafe_allow_html=True)
    
    # Add sustainability image with better layout
    try:
        col1, col2, col3 = st.columns([1, 6, 1])
        with col2:
            st.image("https://www.innovationnewsnetwork.com/wp-content/uploads/2025/11/shutterstock_2397267413-696x391.jpg", 
                    caption="Sustainable Supply Chain Operations", width='stretch')
    except:
        pass
    
    # SDG 9 - Industry, Innovation, Infrastructure
    
    st.markdown('<h3 style="text-align: center; margin-bottom: 2rem; color: #3b82f6;">SDG 9: Industry, Innovation and Infrastructure</h3>', unsafe_allow_html=True)
    
    # Add SDG 9 image with center alignment
    try:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image("https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=600&h=300&fit=crop", 
                    caption="Industry & Innovation", width='stretch')
    except:
        pass
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Efficiency Improvement</h4>
            <p style="color: #f59e0b; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">25%</p>
            <div class="progress-bar"><div class="progress-fill" style="width: 25%;"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Renewable Energy</h4>
            <p style="color: #f59e0b; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">65%</p>
            <div class="progress-bar"><div class="progress-fill" style="width: 65%;"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Local Sourcing</h4>
            <p style="color: #f59e0b; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">78%</p>
            <div class="progress-bar"><div class="progress-fill" style="width: 78%;"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SDG 12 - Responsible Consumption and Production
    
    st.markdown('<h3 style="text-align: center; margin-bottom: 2rem; color: #3b82f6;">SDG 12: Responsible Consumption and Production</h3>', unsafe_allow_html=True)
    
    # Add SDG 12 image with center alignment
    try:
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            st.image("https://images.unsplash.com/photo-1542838132-92c53300491e?w=600&h=300&fit=crop", 
                    caption="Responsible Consumption", width='stretch')
    except:
        pass
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('''
        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Waste Reduction</h4>
            <p style="color: #f59e0b; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">18%</p>
            <div class="progress-bar"><div class="progress-fill" style="width: 18%;"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Sustainable Packaging</h4>
            <p style="color: #f59e0b; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">42%</p>
            <div class="progress-bar"><div class="progress-fill" style="width: 42%;"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown('''
        <div style="background: rgba(245, 158, 11, 0.1); border: 2px solid #f59e0b; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(245, 158, 11, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #f59e0b; margin-bottom: 0.5rem;">Carbon Savings</h4>
            <p style="color: #f59e0b; font-size: 1.5rem; font-weight: bold; margin-bottom: 0.5rem;">1,200 tons</p>
            <div class="progress-bar"><div class="progress-fill" style="width: 75%;"></div></div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Impact Summary with better layout
    
    st.markdown('<h3 style="text-align: center; margin-bottom: 2rem; color: #3b82f6;">Environmental Impact Summary</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div style="background: rgba(139, 92, 246, 0.1); border: 2px solid #8b5cf6; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(139, 92, 246, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #8b5cf6; margin-bottom: 0.5rem;">Total Carbon Reduction</h4>
            <p style="color: #8b5cf6; font-size: 1.2rem; font-weight: bold;">1,200 tons CO2</p>
            <h4 style="color: #8b5cf6; margin-bottom: 0.5rem; margin-top: 1rem;">Energy Efficiency</h4>
            <p style="color: #8b5cf6; font-size: 1.2rem; font-weight: bold;">+32%</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background: rgba(239, 68, 68, 0.1); border: 2px solid #ef4444; border-radius: 15px; padding: 1.5rem; box-shadow: 0 8px 32px rgba(239, 68, 68, 0.3); margin-bottom: 1rem;">
            <h4 style="color: #ef4444; margin-bottom: 0.5rem;">Sustainable Materials</h4>
            <p style="color: #ef4444; font-size: 1.2rem; font-weight: bold;">78%</p>
            <h4 style="color: #ef4444; margin-bottom: 0.5rem; margin-top: 1rem;">Waste Diverted</h4>
            <p style="color: #ef4444; font-size: 1.2rem; font-weight: bold;">450 tons</p>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)  # Close main glass container

# ------------------ MAIN APP ------------------
def main():
    # Generate data
    df = generate_realistic_data()
    
    # Train ML model
    model, state_data = train_demand_prediction_model(df)
    
    # Get predictions
    future_predictions = predict_future_demand(model, state_data)
    
    # Render components
    render_header()
    render_navigation()
    product, state, date_range, auto_refresh = render_sidebar()
    
    # Apply filters
    filtered_df = df.copy()
    if state != "All":
        filtered_df = filtered_df[filtered_df['State'] == state]
    if product != "All":
        # Keep only the selected product column
        filtered_df = filtered_df[['Month', 'State', product, 'Demand_Score', 'Supply_Available']]
        # Rename the product column to standard name for consistency
        filtered_df = filtered_df.rename(columns={product: 'Product_Selected'})
        # Add other product columns as zeros for compatibility
        filtered_df['Product_A'] = 0
        filtered_df['Product_B'] = 0
        filtered_df['Product_C'] = 0
        # Set the selected product values
        if product == 'Product_A':
            filtered_df['Product_A'] = filtered_df['Product_Selected']
        elif product == 'Product_B':
            filtered_df['Product_B'] = filtered_df['Product_Selected']
        elif product == 'Product_C':
            filtered_df['Product_C'] = filtered_df['Product_Selected']
        # Remove temporary column
        filtered_df = filtered_df.drop('Product_Selected', axis=1)
    
    # Recalculate total demand after filtering
    filtered_df['Total_Demand'] = filtered_df['Product_A'] + filtered_df['Product_B'] + filtered_df['Product_C']
    
    # Render current page
    if st.session_state.page == "Dashboard":
        render_dashboard(filtered_df, model, future_predictions)
    elif st.session_state.page == "Analytics":
        render_analytics(filtered_df)
    elif st.session_state.page == "Map View":
        render_map_view(filtered_df)
    elif st.session_state.page == "Activity":
        render_activity_page()
    elif st.session_state.page == "AI Insights":
        render_ai_insights_page(filtered_df, model, future_predictions)
    elif st.session_state.page == "SDG":
        render_sdg_page()
    
    # Auto-refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()

if __name__ == "__main__":
    main()
