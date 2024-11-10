# Third party imports
import yfinance as yf


class TickerProfit:

    def __init__(self):
        pass

    def router(self, cfg):
        
        self.cfg = cfg
        self.calculate_profit(cfg)

        return cfg

    def calculate_profit(self, cfg):

        ticker = cfg['input']['ticker']
        initial_investment = cfg['parameters']['initial_investment']
        start_date = cfg['parameters']['start_date']
        end_date = cfg['parameters']['end_date']

        stock_ticker_object = yf.Ticker(ticker)
        dividends = stock_ticker_object.dividends

        price_data = yf.download(ticker, start=start_date, end=end_date,interval='1d') 

        price_data['Price Change %'] = price_data['Adj Close'].iloc[:].subtract(price_data['Adj Close'].iloc[0]) 

        price_data['overall_profit'] = price_data['Price Change %'] * (initial_investment / 100)
        price_data['value'] = price_data['overall_profit'].add(initial_investment)

        print(price_data)
        csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'
        price_data.to_csv(f'{csv_path}\\overall_profit_{ticker}.csv', index=False)