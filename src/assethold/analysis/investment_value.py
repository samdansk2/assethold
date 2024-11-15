# Third party imports
import pandas as pd
import yfinance as yf


class InvestmentValue:

    def __init__(self):
        pass

    def router(self, cfg):

        self.cfg = cfg
        self.calculate_profit(cfg)

        return cfg

    def calculate_profit(self, cfg):

        # Data
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
            "% profit": ((total_value_monthly - total_invested_monthly) / total_invested_monthly) * 100,
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

    def single_investment_value_calculation(cfg):
        '''
        Calcuate single investement value with time
        A dataframe with daily price, unit bought, value of investment, profit and % profit
        '''
        pass
    
    def multiple_investment_value_calculation(cfg):
        '''
        Calcuate multiple investement value with time
        Assume investment is done on a monthly basis 
        Other investment intervals: semi-monthly, 1 month low, 2 month low, 3 month low, 6 month low, 1 year low
        A dataframe with daily price, unit bought, value of investment, profit and % profit
        '''
        pass
