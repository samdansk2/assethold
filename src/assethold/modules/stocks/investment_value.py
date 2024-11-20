# Third party imports
import pandas as pd


class InvestmentValue:

    def __init__(self):
        pass

    def router(self, cfg, daily_data):

        self.single_investment(cfg, daily_data)
        self.multiple_investment(cfg, daily_data)

        return cfg

    def single_investment(self, cfg, holdings_df):
        
        holdings_df = holdings_df.copy()
        initial_investment = cfg['parameters']['initial_investment']

        self.calculate_single_investment(initial_investment, holdings_df)

    def calculate_single_investment(self, initial_investment, holdings_df):
        '''
        Single investement value with time
        A dataframe with daily price, unit bought, value of investment and profit
        '''
        holdings_df['investment'] = initial_investment
        holdings_df['Price Change %'] = holdings_df['Close'].subtract(holdings_df['Close'].iloc[0]) / holdings_df['Close'].iloc[0] * 100
        holdings_df['Units Bought'] = initial_investment / holdings_df['Close']
        holdings_df['Overall Profit'] = holdings_df['Price Change %'] * (initial_investment / 100)
        holdings_df['Value'] = holdings_df['Overall Profit'] + initial_investment

        # Calculate average_annual_invesment
        holdings_df['average_annual_investment'] = 0
        for idx, row in holdings_df.iterrows():
            if idx != 0:
                average_annual_investment_increment = holdings_df.at[idx-1, 'investment']*(row['Date'] - holdings_df['Date'].iloc[idx-1]).days/365
                average_annual_investment = holdings_df.at[idx-1, 'average_annual_investment'] + average_annual_investment_increment
                holdings_df.at[idx, 'average_annual_investment'] = average_annual_investment

        holdings_df['average_days'] = holdings_df['investment']*(holdings_df['Date'] - holdings_df['Date'].iloc[0]).dt.days

        holdings_df['annual_profit'] = (holdings_df['Value'] - holdings_df['investment'])/holdings_df['average_annual_investment']*100

        self.save_results(holdings_df, 'single_investment.csv')
    
    def multiple_investment(self, cfg, holdings_df):
        
        holdings_df = holdings_df.copy()
        initial_investment = cfg['parameters']['initial_investment']
        
        holdings_df['Date'] = pd.to_datetime(holdings_df['Date'])
        holdings_df = holdings_df.sort_values(by='Date')

        self.calculate_multiple_investment(initial_investment, holdings_df)
        
    def calculate_multiple_investment(self, initial_investment, holdings_df):
        '''
        Calcuate multiple investement value with time
        Assume investment is done on a 'monthly basis' 
        Other investment intervals: semi-monthly, 1 month low, 2 month low, 3 month low, 6 month low, 1 year low
        A dataframe with daily price, unit bought, value of investment and profit
        '''

        holdings_df['Units bought'] = 0.0
        holdings_df['investment'] = 0.0
        holdings_df['Value'] = 0.0

        total_units = 0.0
        total_investment = 0.0
        last_month = None

        for idx, row in holdings_df.iterrows():
            current_month = row['Date'].month

            # Invest on the first occurrence of each month
            if current_month != last_month:
                total_units += initial_investment / row['Close']
                total_investment += initial_investment
                last_month = current_month

            current_value = total_units * row['Close']
            holdings_df.at[idx, 'Units bought'] = total_units
            holdings_df.at[idx, 'investment'] = total_investment
            holdings_df.at[idx, 'Value'] = current_value
        
        holdings_df['Overall Profit'] = holdings_df['Value'] - holdings_df['investment']
        self.save_results(holdings_df, 'multiple_investment.csv')

    def save_results(self, holdings_df, file_name):
        csv_path = r'src\assethold\tests\test_data\modules\stocks\analysis\portfolio\results\Data'
        holdings_df.to_csv(f'{csv_path}\\{file_name}', index=False)

