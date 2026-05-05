import streamlit as st
import pandas as pd

from langgraph.graph import StateGraph, END
from langgraph_flow.state import initial_state
from langgraph_flow.graph import build_graph

# Page configuration
st.set_page_config(
    page_title="EV Battery Health Monitor", 
    layout="wide",
    page_icon="🔋"
)

# Header with styling
st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1 style="color: #2E8B57;">🔋 EV Battery Health Monitoring</h1>
        <h3 style="color: #4682B4;">Agentic AI Workflow Dashboard</h3>
    </div>
""", unsafe_allow_html=True)

# Sidebar styling
st.sidebar.markdown("### 📁 Data Upload")
st.sidebar.markdown("Upload your battery logs to analyze health metrics")

file = st.sidebar.file_uploader(
    "Choose battery_logs.csv file", 
    type=["csv"],
    help="Upload CSV file containing battery data"
)

if file:
    # Load and display data
    df = pd.read_csv(file)
    
    # Data preview section
    with st.container():
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 Battery Data Preview")
            st.dataframe(df.head(), use_container_width=True)
        
        with col2:
            st.markdown("### 📈 Quick Stats")
            st.metric("Total Records", len(df))
            if 'SoH' in df.columns:
                st.metric("Avg SoH", f"{df['SoH'].mean():.1f}%")
            if 'temperature' in df.columns:
                st.metric("Avg Temp", f"{df['temperature'].mean():.1f}°C")

    # Workflow execution
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Run AI Analysis", type="primary", use_container_width=True):
            # Initialize state
            state = initial_state()
            state["battery_data_csv"] = df
            
            # Run workflow with progress
            with st.spinner("Running AI analysis..."):
                final_state = build_graph(state)
            
            st.success("✅ Analysis Complete!")
            
            # Results display
            st.markdown("## 📋 Analysis Results")
            
            # Create tabs for different outputs
            tab1, tab2, tab3 = st.tabs(["🛠️ Service Plan", "📅 Appointment", "✉️ Communication"])
            
            with tab1:
                if "service_plan" in final_state:
                    st.json(final_state["service_plan"])
                else:
                    st.info("No service plan generated")
            
            with tab2:
                if "appointment" in final_state:
                    st.json(final_state["appointment"])
                else:
                    st.info("No appointment scheduled")
            
            with tab3:
                if "user_message" in final_state:
                    st.markdown(f"**Message:** {final_state['user_message']}")
                else:
                    st.info("No communication generated")

else:
    # Welcome screen
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h2>🚗 Welcome to EV Battery Health Monitor</h2>
        <p style="font-size: 18px; color: #666;">
            Upload your battery logs to get started with AI-powered health analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature highlights
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔍 Analysis
        - Battery health insights
        - Anomaly detection
        - Performance trends
        """)
    
    with col2:
        st.markdown("""
        ### 🛠️ Planning
        - Service recommendations
        - Maintenance scheduling
        - Priority assessment
        """)
    
    with col3:
        st.markdown("""
        ### 📱 Communication
        - Automated notifications
        - Status updates
        - Action items
        """)
    
    st.info("👆 Please upload your 'battery_logs.csv' file using the sidebar to begin analysis")