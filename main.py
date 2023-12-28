import dash
from notion_pull import Notion_Puller
from pangea_locator import Pangea_Locator
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output, State, ALL
from pprint import pprint

# Initialize the Dash app
app = dash.Dash(__name__)

# Create the layout of the app
app.layout = html.Div([
    dcc.Graph(id='live-update-map', style={'width': '100%', 'height': '100vh'}),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    ),
    html.Div([
        dcc.Input(id='ip-input', type='text', placeholder='Enter IP Address'),
        html.Button('Add to Database', id='add-button', n_clicks=0),
    ]),
])

# Store the previous IP address and button click count
prev_ip_address = None
prev_n_clicks = 0

# Define the callback to update the map at regular intervals
@app.callback(Output('live-update-map', 'figure'),
              [Input('interval-component', 'n_intervals')],
              [State('add-button', 'n_clicks'),
               State('ip-input', 'value')])
def update_map(n_intervals, n_clicks, ip_address):
    global prev_ip_address, prev_n_clicks

    # Check if the button was clicked and IP address is provided
    if n_clicks is not None and n_clicks > prev_n_clicks and ip_address:
        # Add the IP address to the Notion database (you need to implement this logic)
        notion_add_ip_address(ip_address)
        
        # Store the current IP address and button click count
        prev_ip_address = ip_address
        prev_n_clicks = n_clicks

    # Refresh the data from Notion
    n = Notion_Puller()
    coordinates_array = n.get_data()

    # Update the map figure
    fig = px.scatter_geo(coordinates_array, lat='lat', lon='lon', projection='natural earth', color_discrete_sequence=['red'])
    fig.update_geos(projection_type="natural earth")
    fig.update_layout(title_text='Live Updating World Map')

    return fig

# Function to add IP address to Notion database (you need to implement this)
def notion_add_ip_address(ip_address):
    p = Pangea_Locator()
    result = p.locate([ip_address])
    n = Notion_Puller()
    n.write_row_to_database(ip_address=ip_address, latitude=result['latitude'], longitude=result['longitude'])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)