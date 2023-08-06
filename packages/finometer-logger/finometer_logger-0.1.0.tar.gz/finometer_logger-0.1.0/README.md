# Finometer Logger

## Installation

- Clone this repository with:

``` sh
git clone git@gitlab.com:abdrysdale/finometer-logger.git
```

- Change into the `finometer-logger` directory.
- Install the dependencies either with:

``` sh
poetry install
poetry shell
```

or by manually installing using your preferred method. The installation dependencies are only:
    - `serialdatalog`
    - `numpy`
    - `plotly`
    - `dash`
    - `dash_daq`
    - `toml`

## Usage

The main python script is in `finometer_logger/finometer.py` and to run, simple use:

``` sh
poetry run python finometer_logger/finometer.py
```

or 

``` sh
python finometer_logger/finometer.py
```

By default, the script continously gathers data from the [serialdatalog](https://gitlab.com/abdrysdale/serial-data-logger) database in a background thread whilst plotting the results every 1s in plotly Dash app.

The webapp can be accessed on https://127.0.0.1:8050 and will display the live results of the data logger.

To start collecting data, click the switch above the graph.

To stop collecting data, click the switch again, the data is automatically saved to a csv file with the name as the timestamp the data collection was started - e.g. `t20230530090056.csv` if data collection was started on `30/05/2023 09:00:56`.
