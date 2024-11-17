# Third party imports
import pandas as pd


class InvestmentValue:

    def __init__(self):
        pass

    def router(self, cfg, daily_data):

        self.cfg = cfg
        self.single_investment_value(cfg, daily_data)
        self.multiple_investment_value(cfg, daily_data)

        return cfg

    def single_investment_value(self, cfg, ticker_data):
        '''
        Single investement value with time
        A dataframe with daily price, unit bought, value of investment and profit
        '''
        ticker_data = ticker_data.copy()
        initial_investment = cfg['parameters']['initial_investment']

        ticker_data['Price Change %'] = ticker_data['Close'].subtract(ticker_data['Close'].iloc[0]) / ticker_data['Close'].iloc[0] * 100
        ticker_data['Units Bought'] = initial_investment / ticker_data['Close']
        ticker_data['Overall Profit'] = ticker_data['Price Change %'] * (initial_investment / 100)
        ticker_data['Value'] = ticker_data['Overall Profit'] + initial_investment

        csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'
        ticker_data.to_csv(f'{csv_path}\\single_investment.csv', index=False)
    
    def multiple_investment_value(self, cfg, ticker_data):
        '''
        Multiple investement value with time i.e, monthly investment
        this is investment done on a monthly basis 
        A dataframe with daily price, unit bought, value of investment and profit
        '''
        ticker_data = ticker_data.copy()
        initial_investment = cfg['parameters']['initial_investment']

        ticker_data['Date'] = pd.to_datetime(ticker_data['Date'])
        ticker_data = ticker_data.sort_values(by='Date')

        ticker_data['Units bought'] = 0.0
        ticker_data['Investment'] = 0.0
        ticker_data['Value'] = 0.0

        total_units = 0.0
        total_investment = 0.0
        last_month = None

        for idx, row in ticker_data.iterrows():

            current_month = row['Date'].month

            if current_month != last_month:
                total_units += initial_investment / row['Close']
                total_investment += initial_investment
                last_month = current_month
            
            current_value = total_units * row['Close']
            ticker_data.at[idx, 'Units bought'] = total_units
            ticker_data.at[idx, 'Investment'] = total_investment
            ticker_data.at[idx, 'Value'] = current_value

        ticker_data['Overall Profit'] = ticker_data['Value'] - ticker_data['Investment']

        csv_path = r'src\assethold\tests\test_data\analysis\Portfolio\results\Data'
        ticker_data.to_csv(f'{csv_path}\\multiple_investment.csv', index=False)


