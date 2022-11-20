from dash import Dash
from dash.dependencies import Input, Output

from dashhtmlgrid.plt_children import get_figure
from dashhtmlgrid.html_layout import get_html_layout
from dashhtmlgrid.data_table import get_dash_table_from_df

from dashhtmlgrid.tests.example_stock_data import get_input_data, get_stock_data_df, get_drop_down_options
from dashhtmlgrid.tests.example_data_table import get_example_data_table_df

from stockhold.common.data import AttributeDict
from stockhold.finance_components import FinanceComponents
from stockhold.stock_charts import StockCharts

from stockhold.test.test_service_stock_analysis_run_all_tickers import \
    stock_analysis_by_ticker

fc = FinanceComponents()
sc = StockCharts()

dropdown_array = fc.fdata.get_tickers_sp500()
dropdown_options = get_drop_down_options(dropdown_array)


def run_analysis_if_required(selected_dropdown_value):
    global fc
    if 'stock_ticker' not in fc.fdata.company_info.keys(
    ) or fc.fdata.company_info['stock_ticker'] != selected_dropdown_value[0]:
        fc = stock_analysis_by_ticker(ticker=selected_dropdown_value[0])


def get_table_0_df(selected_dropdown_value):
    run_analysis_if_required(selected_dropdown_value)
    df = fc.fdata.company_info['breakout_trend_indicators'].copy()
    return df


def get_figure_0(selected_dropdown_value):
    run_analysis_if_required(selected_dropdown_value)

    df = fc.fanalysis.ta.copy()

    plot_cfg = {'df': df, 'ticker': selected_dropdown_value[0]}
    plotly_data = sc.get_price_chart(plot_cfg)

    return plotly_data


# Test scripts for Example Operations
df = get_table_0_df(['A'])
plotly_data = get_figure_0(['A'])

# Dashboard custom settings
grid_array = ['dropdown', 'table', 'figure', 'figure']

figure_settings = [{
    'id': 'figure_0',
    'trace': {
        'data_source': None,
        'filter_column': 'stock',
        'filter_value': None,
        'x': 'Date',
        'y': 'value'
    },
    'title': {
        'text': 'Price'
    }
}, {
    'id': 'figure_1',
    'trace': {
        'data_source': None,
        'filter_column': 'stock',
        'filter_value': None,
        'x': 'Date',
        'y': 'change'
    },
    'title': {
        'text': 'Daily Change'
    }
}]

dropdown_settings = [{
    'id': 'dropdownselector',
    'className': 'dropdownselector',
    "H2": 'Stock Analysis | Hold Strategies',
    "p1": ' ',
    "p2": 'Pick one or more options from the dropdown below.',
    'multiple_flag': True,
    'options': dropdown_options,
    'start_value':
        None    # Optional. None will default to 1st value from dropdown_options
}]

table_settings = [{
    "html_id": 'table_0_html',
    "H2": 'Example Table',
    'id': 'table_0_data',
    "p1": 'Additional description for the table',
}]

layout_settings_custom = {
    'grid_array': grid_array,
    'dropdown': dropdown_settings,
    'table': table_settings,
    'figure': figure_settings,
}

# Initialize the app
app = Dash(__name__)
app.config.suppress_callback_exceptions = False

app.layout = get_html_layout(layout_settings_custom)


# Callback for Child Chart #1 (i.e. timeseries price)
@app.callback(Output(figure_settings[0]['id'], 'figure'),
              [Input('dropdownselector', 'value')])
def update_figure_0(selected_dropdown_value):

    plotly_data = get_figure_0(selected_dropdown_value)

    return plotly_data


# # Callback for Child Chart #2 (i.e. Change Chart)
# @app.callback(Output(figure_settings[1]['id'], 'figure'),
#               [Input('dropdownselector', 'value')])
# def update_figure_1(selected_dropdown_value):

#     data_source = get_input_data()
#     figure_1_df = data_source['df'].copy()
#     figure = get_figure(figure_1_df,
#                         selected_dropdown_value,
#                         figure_settings,
#                         figure_idx=1)

#     return figure


# Callback for Table #1 (i.e. Example table)
@app.callback(Output(table_settings[0]['html_id'], 'children'),
              [Input('dropdownselector', 'value')])
def update_table_0(selected_dropdown_value):

    table_0_df = get_table_0_df(selected_dropdown_value)
    table = get_dash_table_from_df(table_0_df, table_settings, table_idx=0)

    return table


if __name__ == '__main__':
    app.run_server(debug=True)
