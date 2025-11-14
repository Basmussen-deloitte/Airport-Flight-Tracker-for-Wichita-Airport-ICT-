import os
import csv
from pathlib import Path
import requests

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output

# Paths to data files (relative to this script)
HERE = Path(__file__).parent
WEATHER_FILE = HERE / 'weather_data.txt'

# Standard columns we expect from FlyWichita / CSV
STANDARD_COLUMNS = [
    'Flight_Number','Type','Airline','Origin','Destination',
    'Scheduled_Time','Actual_Time','Status','Gate','Runway','Aircraft_Type'
]

def fetch_weather_open_meteo(lat=37.75, lon=-97.37):
    """Fetch current weather and hourly forecast from Open-Meteo.

    Returns a dict with `current_weather` and `hourly` keys when available.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&hourly=temperature_2m,precipitation"
        "&current_weather=true&timezone=auto"
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"Open-Meteo fetch failed: {e}")
        return {}


def fetch_flights_from_flywichita(url='https://www.flywichita.com/arrivals-departures/'):
    """Fetch live flights from OpenSky Network API for Wichita area.
    
    Returns a DataFrame with flight data (columns may vary from standard set).
    Falls back to empty DataFrame with standard columns on any error.
    """
    # Wichita area bounding box (latitude, longitude)
    wichita_bbox = (37.45, -97.57, 38.05, -97.17)
    
    try:
        # OpenSky Network API endpoint (free tier, no auth required)
        api_url = "https://opensky-network.org/api/states/all"
        params = {
            'lamin': wichita_bbox[0],
            'lomin': wichita_bbox[1],
            'lamax': wichita_bbox[2],
            'lomax': wichita_bbox[3]
        }
        
        r = requests.get(api_url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        
        flights_list = []
        if data.get('states'):
            for state in data['states']:
                # Parse OpenSky state vector
                flight_dict = {
                    'Flight_Number': (state[1] or 'Unknown').strip(),  # callsign
                    'Type': 'Arrival' if state[14] == 1 else 'Departure',  # on ground
                    'Airline': 'Live Aircraft',
                    'Origin': state[2] or 'Unknown',  # origin country
                    'Destination': 'ICT',
                    'Scheduled_Time': 'N/A',
                    'Actual_Time': 'N/A',
                    'Status': 'In Flight',
                    'Gate': 'N/A',
                    'Runway': 'N/A',
                    'Aircraft_Type': 'Aircraft',
                }
                flights_list.append(flight_dict)
        
        df = pd.DataFrame(flights_list)
        if df.shape[0] > 0:
            print(f"Fetched {len(flights_list)} live flights from OpenSky Network")
        else:
            df = pd.DataFrame(columns=STANDARD_COLUMNS)
        return df
    except Exception as e:
        print(f"Could not fetch flights from OpenSky Network: {e}")
        df = pd.DataFrame(columns=STANDARD_COLUMNS)
        return df


def load_flights():
    """Load flights into a DataFrame.

    This function always fetches live data from FlyWichita. If the fetch fails
    or returns no rows, it returns an empty DataFrame with standard columns.
    """
    df = fetch_flights_from_flywichita()

    # Ensure Scheduled_Hour exists
    if 'Scheduled_Time' in df.columns and 'Scheduled_Hour' not in df.columns:
        def extract_hour(t):
            try:
                return int(str(t).split(':')[0])
            except Exception:
                return None
        df['Scheduled_Hour'] = df['Scheduled_Time'].apply(extract_hour)

    return df


app = Dash(__name__)
server = app.server

# Load data
df = load_flights()

# Prepare initial figures (empty-friendly)
if df is None or df.shape[0] == 0 or 'Status' not in df.columns:
    fig_status = {'data': [], 'layout': {'title': 'No status data available'}}
else:
    status_counts = df['Status'].fillna('Unknown').value_counts().reset_index()
    status_counts.columns = ['Status', 'Count']
    fig_status = px.bar(status_counts, x='Status', y='Count', title='Flights by Status')

if df is None or df.shape[0] == 0 or 'Scheduled_Hour' not in df.columns:
    fig_hour = {'data': [], 'layout': {'title': 'No hour data available'}}
else:
    hour_counts = df['Scheduled_Hour'].dropna().astype(int).value_counts().sort_index().reset_index()
    hour_counts.columns = ['Hour', 'Count']
    fig_hour = px.bar(hour_counts, x='Hour', y='Count', title='Flights by Scheduled Hour')

app.layout = html.Div([
    html.H2('Flight Tracker — Plotly + Dash Starter'),
    html.Div([
        html.Label('Select Chart'),
        dcc.Dropdown(id='chart-type',
                     options=[{'label': 'By Status', 'value': 'status'},
                              {'label': 'By Scheduled Hour', 'value': 'hour'}],
                     value='status')
    ], style={'width': '300px'}),
    
    # Auto-refresh every 15 seconds
    dcc.Interval(id='interval-component', interval=15000, n_intervals=0),
    dcc.Graph(id='main-chart', figure=fig_status),
    html.H3('Flights Data (first 50 rows)'),
    dash_table.DataTable(
        id='flights-table',
        columns=[{"name": c, "id": c} for c in (df.columns if df.shape[0] > 0 else STANDARD_COLUMNS)],
        data=(df.head(50).to_dict('records') if df.shape[0] > 0 else []),
        page_size=10,
        style_table={'overflowX': 'auto'},
    ),
    html.Div(id='debug')
])


@app.callback(
    Output('main-chart', 'figure'),
    Output('flights-table', 'data'),
    Input('chart-type', 'value'),
    Input('interval-component', 'n_intervals')
)
def refresh_chart_and_table(chart_type, n_intervals):
    """Refresh figures and table data when the dropdown changes or the interval ticks.

    Returns (figure, table_data)
    """
    # Fetch latest data
    df_live = load_flights()

    # Recompute figures from live data
    status_counts = df_live.get('Status')
    if status_counts is not None:
        status_counts = df_live['Status'].fillna('Unknown').value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_status_local = px.bar(status_counts, x='Status', y='Count', title='Flights by Status')
    else:
        fig_status_local = {'data': [], 'layout': {'title': 'No status data'}}

    if 'Scheduled_Hour' in df_live.columns:
        hour_counts = df_live['Scheduled_Hour'].dropna().astype(int).value_counts().sort_index().reset_index()
        hour_counts.columns = ['Hour', 'Count']
        fig_hour_local = px.bar(hour_counts, x='Hour', y='Count', title='Flights by Scheduled Hour')
    else:
        fig_hour_local = {'data': [], 'layout': {'title': 'No hour data'}}

    if chart_type == 'status':
        fig = fig_status_local
    else:
        fig = fig_hour_local

    table_data = df_live.head(50).to_dict('records')
    return fig, table_data


if __name__ == '__main__':
    # Runs on http://127.0.0.1:8050 by default
    app.run_server(debug=True, port=8050)
