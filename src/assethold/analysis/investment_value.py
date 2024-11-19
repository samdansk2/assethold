# Third party imports
import pandas as pd


class InvestmentValue:

    def __init__(self):
        pass

    def router(self, cfg, daily_data):

        self.single_investment(cfg, daily_data)
        self.multiple_investment(cfg, daily_data)

        return cfg

    def single_investment(self, cfg, ticker_data):
        
        ticker_data = ticker_data.copy()
        initial_investment = cfg['parameters']['initial_investment']

        self.calculate_single_investment(initial_investment, ticker_data)

    def calculate_single_investment(self, initial_investment, ticker_data):
        '''
        Single investement value with time
        A dataframe with daily price, unit bought, value of investment and profit
        '''
        ticker_data['Investment'] = initial_investment
        ticker_data['Price Change %'] = ticker_data['Close'].subtract(ticker_data['Close'].iloc[0]) / ticker_data['Close'].iloc[0] * 100
        ticker_data['Units Bought'] = initial_investment / ticker_data['Close']
        ticker_data['Overall Profit'] = ticker_data['Price Change %'] * (initial_investment / 100)
        ticker_data['Value'] = ticker_data['Overall Profit'] + initial_investment

        # Calculate average_annual_invesment
        ticker_data['average_annual_investment'] = 0
        for idx, row in ticker_data.iterrows():
            if idx != 0:
                average_annual_investment_increment = ticker_data.at[idx-1, 'Investment']*(row['Date'] - ticker_data['Date'].iloc[idx-1]).days/365
                average_annual_investment = ticker_data.at[idx-1, 'average_annual_investment'] + average_annual_investment_increment
                ticker_data.at[idx, 'average_annual_investment'] = average_annual_investment

        ticker_data['average_days'] = ticker_data['Investment']*(ticker_data['Date'] - ticker_data['Date'].iloc[0]).dt.days

        ticker_data['annual_profit'] = (ticker_data['Value'] - ticker_data['Investment'])/ticker_data['average_annual_investment']*100

        self.save_results(ticker_data, 'single_investment.csv')
    
    def multiple_investment(self, cfg, ticker_data):
        
        ticker_data = ticker_data.copy()
        initial_investment = cfg['parameters']['initial_investment']
        
        ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
        ticker_data = ticker_data.sort_values(by='Date')

        self.calculate_multiple_investment(initial_investment, ticker_data)
        
    def calculate_multiple_investment(self, initial_investment, ticker_data):
        '''
        Calcuate multiple investement value with time
        Assume investment is done on a 'monthly basis' 
        Other investment intervals: semi-monthly, 1 month low, 2 month low, 3 month low, 6 month low, 1 year low
        A dataframe with daily price, unit bought, value of investment and profit
        '''

        ticker_data['Units bought'] = 0.0
        ticker_data['Investment'] = 0.0
        ticker_data['Value'] = 0.0

        total_units = 0.0
        total_investment = 0.0
        last_month = None

        for idx, row in ticker_data.iterrows():
            current_month = row['Date'].month

            # Invest on the first occurrence of each month
            if current_month != last_month:
                total_units += initial_investment / row['Close']
                total_investment += initial_investment
                last_month = current_month

            current_value = total_units * row['Close']
            ticker_data.at[idx, 'Units bought'] = total_units
            ticker_data.at[idx, 'Investment'] = total_investment
            ticker_data.at[idx, 'Value'] = current_value
        
        ticker_data['Overall Profit'] = ticker_data['Value'] - ticker_data['Investment']
        self.save_results(ticker_data, 'multiple_investment.csv')

    def save_results(self, ticker_data, file_name):
        csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'
        ticker_data.to_csv(f'{csv_path}\\{file_name}', index=False)

