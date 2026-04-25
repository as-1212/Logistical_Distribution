"""
Enhanced Map Visualization for Smart Logistics Dashboard
Provides accurate India map with state-level demand visualization
"""

import json
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

import os
from dotenv import load_dotenv

load_dotenv()
px.set_mapbox_access_token(os.getenv("MAPBOX_TOKEN"))

# Complete Indian State Coordinates (Centroid)
INDIA_STATE_COORDINATES = {
    'Andhra Pradesh': [15.9129, 79.7400],
    'Arunachal Pradesh': [28.2180, 94.7278],
    'Assam': [26.2006, 92.9376],
    'Bihar': [25.0961, 85.3131],
    'Chhattisgarh': [21.2787, 81.8661],
    'Delhi': [28.7041, 77.1025],
    'Goa': [15.2993, 73.8243],
    'Gujarat': [23.0225, 72.5714],
    'Haryana': [29.0588, 76.0856],
    'Himachal Pradesh': [31.7433, 77.1205],
    'Jharkhand': [23.6102, 85.2799],
    'Karnataka': [15.3173, 75.7139],
    'Kerala': [10.8505, 76.2711],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Maharashtra': [19.7515, 75.7139],
    'Manipur': [24.6637, 93.9063],
    'Meghalaya': [25.4670, 91.3662],
    'Mizoram': [23.1645, 92.9376],
    'Nagaland': [26.1584, 94.5624],
    'Odisha': [20.9517, 85.0985],
    'Punjab': [31.1471, 75.3412],
    'Rajasthan': [27.5912, 75.7873],
    'Sikkim': [27.5330, 88.5122],
    'Tamil Nadu': [11.1271, 79.2197],
    'Telangana': [18.1124, 79.0193],
    'Tripura': [23.4408, 91.9882],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Uttarakhand': [30.0668, 79.0193],
    'West Bengal': [24.4272, 88.3953]
}

def create_india_map(data_df, title="India Demand Distribution Map"):
    """
    Create an interactive map showing demand distribution across Indian states
    
    Parameters:
    -----------
    data_df : DataFrame
        Must contain columns: 'State', 'Demand_Score', and optionally others for hover
    
    Returns:
    --------
    fig : plotly figure
    """
    
    # Ensure state names match our coordinates
    data_df = data_df.copy()
    
    # Add coordinates
    data_df['lat'] = data_df['State'].map(lambda x: INDIA_STATE_COORDINATES.get(x, [20, 77])[0])
    data_df['lon'] = data_df['State'].map(lambda x: INDIA_STATE_COORDINATES.get(x, [20, 77])[1])
    
    # Create color categories based on demand
    def get_demand_level(score):
        if score > 3.5:
            return 'Critical'
        elif score > 2.5:
            return 'High'
        elif score > 1.5:
            return 'Moderate'
        elif score > 0.5:
            return 'Low'
        else:
            return 'None'
    
    data_df['demand_level'] = data_df['Demand_Score'].apply(get_demand_level)
    
    # Create color map
    color_map = {
        'Critical': '#EF4444',
        'High': '#F97316',
        'Moderate': '#F59E0B',
        'Low': '#60A5FA',
        'None': '#D1D5DB'
    }
    
    data_df['color'] = data_df['demand_level'].map(color_map)
    
    # Create hover text
    data_df['hover_text'] = data_df.apply(
        lambda row: f"<b>{row['State']}</b><br>" +
                   f"Demand Score: {row['Demand_Score']:.1f}<br>" +
                   f"Level: {row['demand_level']}<br>",
        axis=1
    )
    
    # Create scatter mapbox
    fig = go.Figure()
    
    # Add markers for each state
    fig.add_trace(go.Scattermapbox(
        lon=data_df['lon'],
        lat=data_df['lat'],
        mode='markers+text',
        marker=dict(
            size=data_df['Demand_Score'] * 8,  # Size proportional to demand
            color=data_df['color'],
            opacity=0.8,
            line=dict(width=2, color='white'),
            sizemode='diameter'
        ),
        text=data_df['State'],
        textposition='top center',
        textfont=dict(size=9, color='#1F2937'),
        hovertext=data_df['hover_text'],
        hoverinfo='text',
        name='States'
    ))
    
    # Update layout for better visualization
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        height=500,
        mapbox=dict(
            style='dark',
            center=dict(lat=20, lon=78),
            zoom=4.3,
            accesstoken=MAPBOX_TOKEN
        ),
        hovermode='closest',
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        showlegend=False
    )
    
    return fig

def create_demand_comparison_map(data_df, metric='Demand_Score'):
    """
    Create a comparison map with customizable metrics
    """
    
    data_df = data_df.copy()
    data_df['lat'] = data_df['State'].map(lambda x: INDIA_STATE_COORDINATES.get(x, [20, 77])[0])
    data_df['lon'] = data_df['State'].map(lambda x: INDIA_STATE_COORDINATES.get(x, [20, 77])[1])
    
    fig = px.scatter_mapbox(
        data_df,
        lat='lat',
        lon='lon',
        hover_name='State',
        color=metric,
        size=metric,
        color_continuous_scale='Reds',
        size_max=40,
        zoom=4,
        center={'lat': 20, 'lon': 78},
        mapbox_style='dark'
    )
    
    fig.update_layout(
        height=500,
        mapbox_accesstoken=MAPBOX_TOKEN,
        title_text=f"India Demand Distribution - {metric}",
        title_x=0.5
    )
    
    return fig

def get_state_coordinates(state_name):
    """Get coordinates for a specific state"""
    return INDIA_STATE_COORDINATES.get(state_name, [20, 77])

def get_all_states():
    """Get list of all Indian states"""
    return list(INDIA_STATE_COORDINATES.keys())

# Color palette for consistent visualization
COLOR_PALETTE = {
    'critical': '#EF4444',      # Red
    'warning': '#F59E0B',        # Amber
    'moderate': '#06B6D4',       # Cyan
    'safe': '#10B981',           # Green
    'neutral': '#6B7280'         # Gray
}

def get_demand_color(score):
    """Get color based on demand score"""
    if score > 3.5:
        return COLOR_PALETTE['critical']
    elif score > 2.5:
        return COLOR_PALETTE['warning']
    elif score > 1.5:
        return COLOR_PALETTE['moderate']
    else:
        return COLOR_PALETTE['safe']
