"""A script for logging finometer data from a serial input"""

# Python Imports
import logging
import sqlite3
import time
import csv
from multiprocessing import Process, Manager

# Module imports
import toml
import numpy as np
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_daq as daq
import serialdatalog as sdl

# Sets up logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataSink:
    """A sink for the data recieved from the logger."""
    def __init__(self, db_path, col="Elapsed_Time", length=1000):
        """Initialises a sink for the data recieved from a serial logger

        Args:
            db_path (str) : Path to the database logged from the serial logger.
            col (str, optional) : Column to sort values by to select the most
                recent values. Defaults to 'Elapsed_Time'.
            length (int, optional) : Number of values to display at once.
                Defaults to 1000.
        """

        self.db_path = db_path
        self.col = col
        self.length = length

        con = sqlite3.connect(self.db_path)
        res = con.execute("SELECT name FROM sqlite_master WHERE type='table'")
        self.columns = [d[0] for d in res.description]
        tables = [n for n in res.fetchall()]
        logger.info("The following tables were found from %s: %s", db_path, str(tables))
        self.table = tables[-1][0]
        con.close()

    def get(self):
        """Gets the most last N values where N is the length

        Returns:
            data (dict) : A dictionary of the data from the SQL table.
        """
        con = sqlite3.connect(self.db_path)
        res = con.execute(
            "SELECT * FROM ("
            f"SELECT * FROM {self.table} ORDER BY {self.col} DESC LIMIT {self.length})"
            f"ORDER BY {self.col};"
        )
        results = res.fetchall()
        con.close()

        fetched_data = np.array(results)
        data = {str(i) : fetched_data[:, i] for i in range(fetched_data.shape[1])}
        return data

    def to_csv(self):
        """Write the SQL table to a csv file.

        The CSV file is named the same name as the SQL table appened with a .csv
        """
        con = sqlite3.connect(self.db_path)
        cursor = con.cursor()
        cursor.execute(f"SELECT * from {self.table};")
        with open(f"{self.table}.csv", "w", newline='') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(cursor)
        return True


def draw_graph(data, fig=None, titles=None):
    """Draws graphs from data

    data (dict) : A dictionary containing the data to plot.
        Expected in the format subplot_name : (x_data, y_data)
    fig (plotly figure) : If None, will create a new figure. Else will update the specified figure.
        Defaults to None.
    """

    # Gets the number of rows and columns for graph plotting.
    num_graphs = len(list(data.keys()))
    num_rows = int(np.ceil(np.sqrt(num_graphs)))
    num_cols = int(np.ceil(num_graphs / num_rows))

    if titles is None:
        titles = [f"Signal {i}" for i in range(num_graphs)]

    if fig is None:
        fig = make_subplots(rows=num_rows, cols=num_cols, subplot_titles=titles)
        for i, key in enumerate(list(data.keys())):
            row = int(np.floor(i / num_cols) + 1)
            col = i % (num_cols) + 1
            fig.add_scatter(x=np.arange(data[key].size), y=data[key], mode="lines", name=key, row=row, col=col)
    else:
        for i, key in enumerate(list(data.keys())):
            row = int(np.floor(i / num_cols) + 1)
            col = i % (num_cols) + 1
            fig.update_traces(overwrite=True, x=np.arange(data[key].size), y=data[key], mode="lines", row=row, col=col)

    return fig

######## MAIN SCRIPT #########
MANAGER = Manager()
TRIGGER = MANAGER.Value('b', False)
CONFIG = toml.load("config.toml")

# Sets up the dash web app
app = dash.Dash()
app.layout = html.Div([
    html.H1(children="Finometer Datalogger", style={'textAlign':'center'}),
    daq.ToggleSwitch(id='collect-data', value=TRIGGER.value),
    html.Div(id='toggle-output'),
    dcc.Graph(id='plot'),
    dcc.Interval(
        id="interval-component",
        interval=1e3,
        n_intervals=0,
    ),
])

@app.callback(
    Output('plot', 'figure'),
    Input('interval-component', 'n_intervals'),
    Input('collect-data', 'value'),
    Input('toggle-output', 'children'),
)
def fig(n, trigger, msg):
    """Plots a figure"""
    titles = list(CONFIG["table_dict"].keys())
    titles.append("Timestamp")

    if trigger and msg == 'Running':
        data = SINK.get()
        fig = draw_graph(data, titles=titles)
    else:
        fig = make_subplots(1, 1)
    return fig

@app.callback(
    Output('toggle-output', 'children'),
    Input('collect-data', 'value')
)
def switch(value):
    """Controls the figure"""
    global SERIAL_LOGGER
    global SINK

    TRIGGER.value = value

    if value:
        SERIAL_LOGGER = Process(
            target=sdl.logger,
            args=(CONFIG["table_dict"], CONFIG["source"], CONFIG["dest"],),
            kwargs={"trigger" : TRIGGER},
        )
        SERIAL_LOGGER.start()
        time.sleep(1) # Delay to allow for database/table creation
        SINK = DataSink(CONFIG["dest"], length=1000)
        return 'Running'
    try:
        SINK.to_csv()
    except Exception as error:
        logger.info(error)
    return 'Stopped'


# Runs the main script
if __name__ == "__main__":
    app.run_server()
