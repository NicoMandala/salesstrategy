import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Set page config
st.set_page_config(
    page_title="LinkedIn Analytics Dashboard",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric > label {
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    .stMetric > div {
        font-size: 24px !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

def extract_first_sentence(text):
    """Extract the first sentence from post title"""
    if pd.isna(text) or text == "":
        return ""
    
    # Split by common sentence endings
    sentences = re.split(r'[.!?]\s+', str(text))
    first_sentence = sentences[0].strip()
    
    # If the first sentence is very short, try to get more context
    if len(first_sentence) < 20 and len(sentences) > 1:
        first_sentence = sentences[0] + ". " + sentences[1]
    
    # Limit length for display
    if len(first_sentence) > 100:
        first_sentence = first_sentence[:97] + "..."
    
    return first_sentence

def load_and_process_data(uploaded_file):
    """Load and process the LinkedIn analytics data"""
    try:
        # Read the Excel file, skipping the first row to use the second row as the header
        df = pd.read_excel(uploaded_file, sheet_name='All posts', header=1)
        
        # Standardize column names to lowercase and strip whitespace
        df.columns = [str(col).lower().strip() for col in df.columns]

        # Check for essential column 'post title'
        if 'post title' not in df.columns:
            st.error("Error: 'Post title' column not found. Please ensure your Excel file has this column.")
            return None

        # Clean and process the data
        df['post title (first sentence)'] = df['post title'].apply(extract_first_sentence)
        
        # Convert date column
        if 'created date' in df.columns:
            df['created date'] = pd.to_datetime(df['created date'])
        
        # Convert percentage columns to numeric
        if 'engagement rate' in df.columns:
            df['engagement rate'] = pd.to_numeric(df['engagement rate'], errors='coerce')
        
        if 'click through rate (ctr)' in df.columns:
            df['click through rate (ctr)'] = pd.to_numeric(df['click through rate (ctr)'], errors='coerce')
        
        # Convert impressions to numeric
        if 'impressions' in df.columns:
            df['impressions'] = pd.to_numeric(df['impressions'], errors='coerce')
        
        return df
    
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

def create_summary_metrics(df):
    """Create summary metrics cards"""
    total_posts = len(df)
    avg_engagement = df['engagement rate'].mean() * 100 if 'engagement rate' in df.columns else 0
    avg_ctr = df['click through rate (ctr)'].mean() * 100 if 'click through rate (ctr)' in df.columns else 0
    total_impressions = df['impressions'].sum() if 'impressions' in df.columns else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 Total Posts",
            value=f"{total_posts:,}"
        )
    
    with col2:
        st.metric(
            label="👁️ Total Impressions",
            value=f"{total_impressions:,}"
        )
    
    with col3:
        st.metric(
            label="💬 Avg Engagement Rate",
            value=f"{avg_engagement:.2f}%"
        )
    
    with col4:
        st.metric(
            label="🔗 Avg Click-Through Rate",
            value=f"{avg_ctr:.2f}%"
        )

def create_engagement_trend_chart(df):
    """Create engagement trend over time"""
    if 'created date' not in df.columns:
        return None
    
    # Group by date and calculate average engagement
    daily_stats = df.groupby(df['created date'].dt.date).agg({
        'engagement rate': 'mean',
        'impressions': 'sum',
        'click through rate (ctr)': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=daily_stats['created date'],
        y=daily_stats['engagement rate'] * 100,
        mode='lines+markers',
        name='Engagement Rate (%)',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title="Engagement Rate Trend Over Time",
        xaxis_title="Date",
        yaxis_title="Engagement Rate (%)",
        hovermode='x unified',
        showlegend=True,
        height=400
    )
    
    return fig

def create_top_posts_chart(df, metric='engagement rate', top_n=10):
    """Create top posts chart"""
    if metric not in df.columns:
        return None
    
    # Get top posts
    top_posts = df.nlargest(top_n, metric)[['post title (first sentence)', metric, 'impressions']].copy()
    
    # Convert to percentage if needed
    if metric in ['engagement rate', 'click through rate (ctr)']:
        top_posts[f'{metric} (%)'] = top_posts[metric] * 100
        y_col = f'{metric} (%)'
    else:
        y_col = metric
    
    fig = px.bar(
        top_posts,
        x=y_col,
        y='post title (first sentence)',
        orientation='h',
        title=f"Top {top_n} Posts by {metric.replace('_', ' ').title()}",
        hover_data=['impressions']
    )
    
    fig.update_layout(
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_scatter_plot(df):
    """Create impressions vs engagement scatter plot"""
    if 'impressions' not in df.columns or 'engagement rate' not in df.columns:
        return None
    
    fig = px.scatter(
        df,
        x='impressions',
        y=df['engagement rate'] * 100,
        hover_data=['post title (first sentence)', 'click through rate (ctr)'],
        title="Impressions vs Engagement Rate",
        labels={'y': 'Engagement Rate (%)'}
    )
    
    fig.update_layout(height=400)
    return fig

def main():
    st.title("📊 LinkedIn Analytics Dashboard")
    st.markdown("Upload your LinkedIn content analytics Excel file to visualize your post performance.")
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose your LinkedIn analytics Excel file",
        type=['xlsx', 'xls'],
        help="Upload the Excel file downloaded from LinkedIn (should contain 'All posts' sheet)"
    )
    
    if uploaded_file is not None:
        # Load and process data
        with st.spinner("Loading and processing data..."):
            df = load_and_process_data(uploaded_file)
        
        if df is not None:
            st.success(f"✅ Successfully loaded {len(df)} posts!")
            
            # Summary metrics
            st.markdown("## 📈 Key Metrics")
            create_summary_metrics(df)
            
            # Sidebar filters
            st.sidebar.header("🔍 Filters")
            
            # Post type filter
            if 'post type' in df.columns:
                post_types = ['All'] + list(df['post type'].unique())
                selected_post_type = st.sidebar.selectbox("Post Type", post_types)
                
                if selected_post_type != 'All':
                    df = df[df['post type'] == selected_post_type]
            
            # Date range filter
            if 'created date' in df.columns:
                date_range = st.sidebar.date_input(
                    "Date Range",
                    value=(df['created date'].min().date(), df['created date'].max().date()),
                    min_value=df['created date'].min().date(),
                    max_value=df['created date'].max().date()
                )
                
                if len(date_range) == 2:
                    start_date, end_date = date_range
                    df = df[(df['created date'].dt.date >= start_date) & 
                           (df['created date'].dt.date <= end_date)]
            
            # Charts section
            st.markdown("## 📊 Analytics Charts")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Engagement trend
                trend_fig = create_engagement_trend_chart(df)
                if trend_fig:
                    st.plotly_chart(trend_fig, use_container_width=True)
            
            with col2:
                # Scatter plot
                scatter_fig = create_scatter_plot(df)
                if scatter_fig:
                    st.plotly_chart(scatter_fig, use_container_width=True)
            
            # Top posts charts
            col3, col4 = st.columns(2)
            
            with col3:
                top_engagement_fig = create_top_posts_chart(df, 'engagement rate')
                if top_engagement_fig:
                    st.plotly_chart(top_engagement_fig, use_container_width=True)
            
            with col4:
                top_ctr_fig = create_top_posts_chart(df, 'click through rate (ctr)')
                if top_ctr_fig:
                    st.plotly_chart(top_ctr_fig, use_container_width=True)
            
            # Data table
            st.markdown("## 📋 Post Performance Table")
            
            # Select columns to display
            display_columns = [
                'post title (first sentence)',
                'impressions',
                'engagement rate',
                'click through rate (ctr)'
            ]
            
            # Filter columns that exist in the dataframe
            available_columns = [col for col in display_columns if col in df.columns]
            
            if 'created date' in df.columns:
                available_columns.insert(1, 'created date')
            
            if 'post type' in df.columns:
                available_columns.append('post type')
            
            # Format the display dataframe
            display_df = df[available_columns].copy()
            
            # Format percentage columns
            if 'engagement rate' in display_df.columns:
                display_df['engagement rate'] = (display_df['engagement rate'] * 100).round(2).astype(str) + '%'
            
            if 'click through rate (ctr)' in display_df.columns:
                display_df['click through rate (ctr)'] = (display_df['click through rate (ctr)'] * 100).round(2).astype(str) + '%'
            
            # Format impressions
            if 'impressions' in display_df.columns:
                display_df['impressions'] = display_df['impressions'].apply(lambda x: f"{x:,}" if pd.notna(x) else "0")
            
            # Search functionality
            search_term = st.text_input("🔍 Search posts", placeholder="Enter keywords to search in post titles...")
            
            if search_term:
                mask = display_df['post title (first sentence)'].str.contains(search_term, case=False, na=False)
                display_df = display_df[mask]
            
            # Display the table
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400
            )
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download filtered data as CSV",
                data=csv,
                file_name=f"linkedin_analytics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Additional insights
            st.markdown("## 💡 Quick Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'engagement rate' in df.columns and not df['engagement rate'].empty:
                    best_post = df.loc[df['engagement rate'].idxmax()]
                    st.info(f"**🏆 Best Performing Post:**\n\n{best_post['post title (first sentence)']}\n\n"
                           f"Engagement Rate: {best_post['engagement rate']*100:.2f}%")
            
            with col2:
                if 'impressions' in df.columns and not df['impressions'].empty:
                    most_viewed = df.loc[df['impressions'].idxmax()]
                    st.info(f"**👁️ Most Viewed Post:**\n\n{most_viewed['post title (first sentence)']}\n\n"
                           f"Impressions: {most_viewed['impressions']:,}")
    
    else:
        st.info("👆 Please upload your LinkedIn analytics Excel file to get started!")
        
        # Show sample data format
        st.markdown("### 📋 Expected File Format")
        st.markdown("""
        Your Excel file should contain an **'All posts'** sheet. The app is flexible with column names (e.g., 'Post title', 'post title', 'Post Title' are all fine), but they should include:
        - **Post title**: The full text of your LinkedIn post
        - **Impressions**: Number of times the post was viewed
        - **Engagement rate**: Engagement rate as a decimal (e.g., 0.05 for 5%)
        - **Click through rate (CTR)**: Click-through rate as a decimal
        - **Created date**: When the post was created (optional)
        - **Post type**: Organic, Sponsored, or Total (optional)
        """)

if __name__ == "__main__":
    main()
