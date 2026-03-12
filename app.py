import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, State
from datetime import datetime

# Load the processed data
df = pd.read_csv('processed_sales_data.csv')
df['date'] = pd.to_datetime(df['date'])

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div([
    html.Div([
        html.H1('Pink Morsel Sales Analysis', id='header-title'),
    ], id='header'),

    html.Div([
        # Region Filter
        html.Div([
            html.H4('Filter by Region:'),
            dcc.RadioItems(
                options=[
                    {'label': 'North', 'value': 'north'},
                    {'label': 'East', 'value': 'east'},
                    {'label': 'South', 'value': 'south'},
                    {'label': 'West', 'value': 'west'},
                    {'label': 'All', 'value': 'all'}
                ],
                value='all',
                id='region-filter',
                inline=True
            )
        ], className='control-item'),

        # Date Range Picker
        html.Div([
            html.H4('Select Date Range:'),
            dcc.DatePickerRange(
                id='date-picker',
                min_date_allowed=df['date'].min(),
                max_date_allowed=df['date'].max(),
                start_date=df['date'].min(),
                end_date=df['date'].max()
            )
        ], className='control-item'),

        # Download Button
        html.Div([
            html.Button("Download CSV", id="btn-download", className='download-button'),
            dcc.Download(id="download-dataframe-csv"),
        ], className='control-item')
    ], className='control-container'),

    dcc.Graph(id='sales-graph')
])

# --- Callbacks ---

@app.callback(
    Output('sales-graph', 'figure'),
    [Input('region-filter', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(selected_region, start_date, end_date):
    # Filter by region
    filtered_df = df if selected_region == 'all' else df[df['region'] == selected_region]
    
    # Filter by date range
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]

    # Aggregate sales by month
    monthly_sales = filtered_df.set_index('date').resample('M')['sales'].sum().reset_index()

    fig = px.line(
        monthly_sales,
        x='date',
        y='sales',
        title=f'Monthly Sales of Pink Morsels ({selected_region.capitalize()})',
        labels={'date': 'Date', 'sales': 'Total Sales ($)'},
        template='plotly_white'
    )

    # Customize line color
    fig.update_traces(line_color='#e91e63', line_width=3)

    # Price Increase Marker (2021-01-15)
    price_increase_date = datetime(2021, 1, 15)
    
    # Check if the price increase date is within the selected range
    if pd.to_datetime(start_date) <= price_increase_date <= pd.to_datetime(end_date):
        fig.add_vline(x=price_increase_date, line_dash="dash", line_color="red", line_width=2)
        
        # Position the annotation at the top of the chart
        y_max = monthly_sales['sales'].max() if not monthly_sales.empty else 0
        fig.add_annotation(
            x=price_increase_date,
            y=y_max,
            text="Price Increase",
            showarrow=True,
            arrowhead=1,
            ax=40,
            ay=-30
        )

    return fig

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn-download", "n_clicks"),
    [State('region-filter', 'value'),
     State('date-picker', 'start_date'),
     State('date-picker', 'end_date')],
    prevent_initial_call=True,
)
def download_data(n_clicks, selected_region, start_date, end_date):
    # Apply filters for the download
    filtered_df = df if selected_region == 'all' else df[df['region'] == selected_region]
    filtered_df = filtered_df[(filtered_df['date'] >= start_date) & (filtered_df['date'] <= end_date)]
    
    # Return the CSV file for download
    return dcc.send_data_frame(filtered_df.to_csv, f"pink_morsel_sales_{selected_region}.csv", index=False)

if __name__ == '__main__':
    app.run_server(debug=True)
