# Third party imports
import pandas as pd


class InvestmentValue:

    def __init__(self):
        pass

    def router(self, cfg, daily_data):

        self.single_investment(cfg, daily_data)

        return cfg

    def single_investment(self, cfg, holdings_df):

        holdings_df = holdings_df.copy()
        single_investment_cfg = cfg['investment_settings']

        initial_investment = single_investment_cfg['single']['investment']
        holdings_df['investment'] = initial_investment
        holdings_df['Units Bought'] = initial_investment / holdings_df['Close']
        holdings_df['daily_returns'] = holdings_df['Close'].pct_change()
        holdings_df['Value'] = holdings_df['daily_returns'] + initial_investment

        # Calculate average_annual_invesment
        holdings_df['average_annual_investment'] = 0.0
        for idx, row in holdings_df.iterrows():
            if idx != 0:
                average_annual_investment_increment = holdings_df.at[idx-1, 'investment']*(row['Date'] - holdings_df['Date'].iloc[idx-1]).days/365
                average_annual_investment = holdings_df.at[idx-1, 'average_annual_investment'] + average_annual_investment_increment
                holdings_df.at[idx, 'average_annual_investment'] = average_annual_investment

        holdings_df['average_days'] = holdings_df['investment']*(holdings_df['Date'] - holdings_df['Date'].iloc[0]).dt.days

        holdings_df['annual_profit'] = (holdings_df['Value'] - holdings_df['investment'])/holdings_df['average_annual_investment']*100

        self.save_results(holdings_df, 'single_investment.csv')
        
        return holdings_df

    def multiple_investment(self, cfg, holdings_df):

        #Convert to group of single investments

        #TODO - Implement multiple investment
        
        for idx, row in holdings_df.iterrows():
            single_investment_cfg = {
                'investment': 100,
                'buy_date': row['Date']
            }

        single_holdings_df = holdings_df.copy() # Edit with buy date
        
        single_holdings_df = self.calculate_single_investment(single_investment_cfg, holdings_df)
        
        # multiple_holdings_df = multiple_holdings_df.add_by_date(single_holdings_df)
    
        pass

    def calculate_interest(self, cfg, holdings_df, total_investment):
        """
        Simple and compound interest based on cumulative investment.
        """
        annual_rate =  0.05 # sample interest rate of 5%
        principal = total_investment
        start_date = holdings_df['Date'].iloc[0]
        end_date = holdings_df['Date'].iloc[-1]
        time_in_years = (end_date - start_date).days / 365

        # SI 
        simple_interest = principal * annual_rate * time_in_years

        # CI
        compound_interest = principal * ((1 + annual_rate) ** time_in_years - 1)

        return simple_interest, compound_interest
    
    def save_results(self, holdings_df, file_name):
        csv_path = r'tests\modules\stocks\analysis\investment\results\Data'
        holdings_df.to_csv(f'{csv_path}\\{file_name}', index=False)

