import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from datetime import datetime

# --- Data Preparation ---
df = pd.read_csv('processed_sales_data.csv')
df['date'] = pd.to_datetime(df['date'])
daily_sales = df.groupby('date')['sales'].sum().reset_index()
 
# --- Dash App ---
app = Dash(__name__)

# Create the line chart
fig = px.line(
   daily_sales,
   x='date',
   y='sales',
   title='Daily Sales of Pink Morsels Over Time',
   labels={'date': 'Date', 'sales': 'Total Daily Sales'}
   )
 
 

fig.add_vline(
   x=datetime(2021, 1, 15),
   line_width=2,
   line_dash="dash",
   line_color="red"
   )
 

fig.add_annotation(
   x=datetime(2021, 1, 15),
   y=daily_sales['sales'].max(),  
   text="Price Increase",
   showarrow=False,
   yshift=10  
   )
 



# Define the app layout
app.layout = html.Div([
   html.H1(children='Pink Morsel Sales Analysis', style={'textAlign': 'center'}),
   dcc.Graph(figure=fig)
   ])
 
# Run the app
if __name__ == '__main__':
   app.run_server(debug=True);