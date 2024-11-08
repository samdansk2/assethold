# Third party imports
import yfinance as yf

ticker = 'XOM'  
initial_investment = 100
investment_frequency = 'single'
investment_frequency = '1mo' # monthly
buy_date = '2020-01-01'
start_date = '2020-01-01'
end_date = '2024-11-01'
interval = '1mo'

stock_ticker_object = yf.Ticker(ticker)
dividends = stock_ticker_object.dividends

price_data = yf.download(ticker, start=start_date, end=end_date, interval=interval)

# monthly profit
# data['Price Change %'] = data['Adj Close'].pct_change() * 100 # percentage change
# data['Monthly Profit'] = data['Price Change %'] * (initial_investment / 100)

price_data['Price Change %'] = price_data['Adj Close'].iloc[:].subtract(price_data['Adj Close'].iloc[0])

price_data['overall_profit'] = price_data['Price Change %'] * (initial_investment / 100)
price_data['value'] = price_data['overall_profit'].add(initial_investment)

# df = price_data[['Adj Close', 'Price Change %', 'overall_profit']].dropna().reset_index()
# df.columns = ['Date', 'Adj Close', 'Price Change %', 'overall_profit']

print(price_data)
csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'
price_data.to_csv(f'{csv_path}\\overall_profit_{ticker}.csv', index=False)