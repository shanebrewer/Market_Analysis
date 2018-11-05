from iexfinance import get_historical_data
from datetime import datetime
import pandas as pd
import time
import dash
import dash_core_components as dcc
import dash_html_components as html


START_DATE = datetime(2018, 1, 1)
END_DATE = datetime.now()
BASE_DIRECTORY = "C:\\Users\\Shane\\Dropbox\\PyCharm Projects\\Market_Analysis\\"
DATA_DIRECTORY = BASE_DIRECTORY + "data\\"
#INPUT_DATA_FILENAME = "DataInstruments.csv"
INPUT_DATA_FILENAME = "TestData.csv"
OUTPUT_DIRECTORY = BASE_DIRECTORY + "output\\"
OUTPUT_EXCEL_FILENAME = "Market Data.xlsx"


def read_equity_list_from_csv():
    print("Reading data file: " + DATA_DIRECTORY + INPUT_DATA_FILENAME)
    df = pd.read_csv(DATA_DIRECTORY + INPUT_DATA_FILENAME)
    return df


def get_equity_price_data_from_iex(instruments_df):
    instruments_price_data_df = pd.DataFrame()
    for row in instruments_df.itertuples():
        print("Processing: " + getattr(row, "Instrument"))
        try:
            instrument_df = get_historical_data(getattr(row, 'Instrument'),
                                                start=START_DATE,
                                                end=END_DATE,
                                                output_format='pandas')
            instrument_df = instrument_df.assign(Instrument=getattr(row, 'Instrument'))
            instruments_price_data_df = instruments_price_data_df.append(instrument_df, ignore_index=True)
        except Exception:
            print("Could not process " + getattr(row, "Instrument"))
        time.sleep(.5)
    return instruments_price_data_df


def generate_dash_dashboard(instruments_df):
    app = dash.Dash()
    app.layout = html.Div(children=[
        html.H1('Market Analysis Dashboard'),
        dcc.Graph(
            id='example',
            figure={
                'data': [
                    {'x': instruments_df,
                     'y': instruments_df,
                     'type': 'line',
                     'name': 'S&P500'
                     }
                ],
                'layout': {'title': 'Basic Dash Example'}
            }
        )
    ])

    if __name__ == '__main__':
        app.run_server(debug=True)


instruments_df = read_equity_list_from_csv()
instruments_price_data_df = get_equity_price_data_from_iex(instruments_df)
generate_dash_dashboard(instruments_df)

