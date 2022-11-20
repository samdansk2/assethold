import datetime
import json

from dashhtmlgrid.common.visualization import Visualization


class StockCharts:

    def __init__(self):
        pass

    def get_price_chart(self, cfg):
        viz = Visualization()

        df = cfg['df']
        ticker = cfg['ticker']

        cfg_plot_data = {
            'data_source': df,
            'type': "scatter",
            'mode': "lines",
            'name': ['Close', '50 day avg.', '150 day avg.', '200 day avg.'],
            'x': ['Date'],
            'y': [
                'Close', '50_day_rolling', '150_day_rolling', '200_day_rolling'
            ],
            'line': {
                'color': None
            }
        }
        layout = {
            'title': 'Stock Price Timeline: {}'.format(ticker),
            'xaxis': {
                'title': 'Date',
            },
            'yaxis': {
                'title': 'Value'
            }
        }
        cfg_plot_data.update({'layout': layout})

        plotly_data = viz.get_plotly_data(cfg_plot_data)

        return plotly_data
