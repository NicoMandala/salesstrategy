# LinkedIn Analytics Dashboard

A Streamlit web application for analyzing LinkedIn content performance data from exported Excel files.

## Features

- 📊 **Interactive Dashboard**: Visual analytics with charts and metrics
- 📈 **Key Metrics**: Total posts, impressions, engagement rates, and CTR
- 📋 **Data Table**: Searchable and filterable post performance table
- 🔍 **Filters**: Filter by post type and date range
- 📥 **Export**: Download filtered data as CSV
- 💡 **Insights**: Identify best performing and most viewed posts

## Setup Instructions

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   streamlit run streamlit_app.py
   ```

3. **Open in Browser**
   The app will automatically open in your default browser at `http://localhost:8501`

## How to Use

1. **Prepare Your Data**
   - Export your LinkedIn analytics data as an Excel file
   - Ensure the file contains an "All posts" sheet with these columns:
     - `Post title`: The full text of your LinkedIn post
     - `Impressions`: Number of times the post was viewed
     - `Engagement rate`: Engagement rate as a decimal (e.g., 0.05 for 5%)
     - `Click through rate (CTR)`: Click-through rate as a decimal
     - `Created date`: When the post was created (optional)
     - `Post type`: Organic, Sponsored, or Total (optional)

2. **Upload Your File**
   - Click "Browse files" and select your LinkedIn analytics Excel file
   - The app will automatically process and display your data

3. **Explore Your Analytics**
   - View key metrics at the top of the dashboard
   - Use the sidebar filters to narrow down your analysis
   - Examine the various charts showing engagement trends and top posts
   - Search through your posts in the data table
   - Download filtered results as CSV

## File Structure

```
├── streamlit_app.py      # Main Streamlit application
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── leaf-space_content_1753863379800.xlsx  # Sample LinkedIn data file
```

## Dependencies

- **streamlit**: Web app framework
- **pandas**: Data manipulation and analysis
- **plotly**: Interactive charts and visualizations
- **openpyxl**: Modern Excel file (`.xlsx`) reading support
- **xlrd**: Legacy Excel file (`.xls`) reading support

## Features Explained

### Dashboard Sections

1. **Key Metrics**: Overview cards showing total posts, impressions, average engagement rate, and CTR
2. **Analytics Charts**: 
   - Engagement rate trend over time
   - Impressions vs engagement rate scatter plot
   - Top posts by engagement rate
   - Top posts by click-through rate
3. **Post Performance Table**: Searchable table with all post data
4. **Quick Insights**: Highlights of best performing and most viewed posts

### Data Processing

- Extracts the first sentence from post titles for cleaner display
- Converts percentage values to proper format for visualization
- Handles missing or invalid data gracefully
- Provides date-based filtering and analysis

## Sample Usage

1. Install dependencies: `pip install -r requirements.txt`
2. Run the app: `streamlit run streamlit_app.py`
3. Upload your `leaf-space_content_1753863379800.xlsx` file
4. Explore your LinkedIn analytics with interactive charts and filters

## Troubleshooting

- **File Upload Issues**: Ensure your Excel file (`.xlsx` or `.xls`) has an "All posts" sheet
- **Missing Data**: The app handles missing columns gracefully and shows available data
- **Performance**: Large files may take a moment to process - wait for the success message

## Support

For issues or questions, please check that your Excel file format matches the expected structure described above.
