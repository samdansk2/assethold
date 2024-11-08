import yfinance as yf

ticker = 'XOM'  
initial_investment = 100  
start_date = '2020-01-01'
end_date = '2024-01-01'

data = yf.download(ticker, start=start_date, end=end_date, interval='1mo')

# monthly profit
data['Price Change %'] = data['Adj Close'].pct_change() * 100 # percentage change
data['Monthly Profit'] = data['Price Change %'] * (initial_investment / 100)   

df = data[['Adj Close', 'Price Change %', 'Monthly Profit']].dropna().reset_index()
df.columns = ['Date', 'Adj Close', 'Price Change %', 'Monthly Profit']

print(df)
csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'
df.to_csv(f'{csv_path}\\monthly_profit_{ticker}.csv', index=False)