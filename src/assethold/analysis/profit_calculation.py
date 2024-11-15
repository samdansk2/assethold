# Third party imports
import yfinance as yf

import pandas as pd


class TickerProfit:

    def __init__(self):
        pass

    def router(self, cfg):
        
        self.cfg = cfg
        self.calculate_profit(cfg)

        return cfg

    def calculate_profit(self, cfg):

        ticker = cfg['input']['ticker']
        investment_amount = cfg['parameters']['initial_investment']
        start_date = cfg['parameters']['start_date']
        end_date = cfg['parameters']['end_date']

        stock_data = yf.download(ticker, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError(f"No data found for ticker {ticker} in the given date range.")

        stock_data['Date'] = stock_data.index
        stock_data['Month'] = stock_data['Date'].dt.to_period('M')  # Extract month for grouping

        monthly_data = stock_data.groupby('Month').first()  # Get the first day of each month
        total_months = len(monthly_data)
        total_invested_monthly = total_months * investment_amount
        
        # total value calculation
        monthly_units = (investment_amount / monthly_data['Close']).sum()
        current_price = stock_data['Close'][-1]
        total_value_monthly = monthly_units * current_price
        monthly_results = {
            "total_invested": total_invested_monthly,
            "total_value": total_value_monthly,
            "profit": total_value_monthly - total_invested_monthly,
        }

        total_days = len(stock_data)
        total_invested_daily = total_days * investment_amount
        daily_units = (investment_amount / stock_data['Close']).sum()
        total_value_daily = daily_units * current_price
        daily_results = {
            "total_invested": total_invested_daily,
            "total_value": total_value_daily,
            "profit": total_value_daily - total_invested_daily,
        }
 
        csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'

        monthly_df = pd.DataFrame([monthly_results])
        monthly_df.to_csv(f"{csv_path}/monthly_investment.csv", index=False)

        daily_df = pd.DataFrame([daily_results])
        daily_df.to_csv(f"{csv_path}/daily_investment_.csv", index=False)

        
        