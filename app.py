import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
from datetime import datetime
 

# Load the processed data
df = pd.read_csv('processed_sales_data.csv')

df['date'] = pd.to_datetime(df['date'])
print(f"Number of unique dates: {df['date'].nunique()}")
 
 
# --- App Initialization ---


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Initialize the Dash app with the external stylesheet
app = Dash(__name__, external_stylesheets=external_stylesheets)



# Define the app layout
app.layout = html.Div([
   html.H1(children='Pink Morsel Sales Analysis', style={'textAlign': 'center'}),
 
   html.Div([
    html.H3('Filter by Region:'),
        dcc.RadioItems(
            options=['north', 'east', 'south', 'west', 'all'],
            value='all',  # Default value
            id='region-filter'
        )],
    style={'width': '48%', 'display': 'inline-block'}),
    html.Hr(), 

# The graph component will be updated by the callback
   dcc.Graph(id='sales-graph')
])

# --- Callback Definition ---

# This decorator links the inputs and outputs to the function below
@app.callback(
   Output('sales-graph', 'figure'), 
   Input('region-filter', 'value')  
   )
def update_graph(selected_region):
   if selected_region == 'all': 
    filtered_df = df
   else: 
    filtered_df = df[df['region'] == selected_region]

   # Aggregate sales by month
   monthly_sales = filtered_df.set_index('date').resample('M')['sales'].sum().reset_index()

   # Create the new line chart with the filtered data
   fig = px.line(
        monthly_sales,
        x='date',
        y='sales',
        title=f'Monthly Sales of Pink Morsels in "{selected_region.capitalize()}" Region',
        labels={'date': 'Date', 'sales': 'Total Monthly Sales'}
    )

   # Add the vertical line for the price increase
   fig.add_vline(
        x=datetime(2021, 1, 15),
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

   # Add the annotation for the price increase
   fig.add_annotation(
        x=datetime(2021, 1, 15),
        y=monthly_sales['sales'].max() if not monthly_sales.empty else 0, # Position at top
        text="Price Increase",
        showarrow=False,
        yshift=10
    )

   # Return the updated figure to the dcc.Graph component
   return fig 
 
if __name__ == '__main__':
   app.run_server(debug=True)