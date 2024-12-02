import ffn
import pandas as pd
import matplotlib.pyplot as plt

class InvestmentValueFfn:

    def __init__(self):
        pass

    def router(self, cfg, holdings_df):

        prices_data = self.prepare_data(holdings_df)
        self.get_returns(cfg, prices_data)

        return cfg
        
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        fix up the data for analysis by ensuring the index is a DatetimeIndex.
        """
        if not isinstance(data.index, pd.DatetimeIndex):
            if 'Date' in data.columns:
                # Convert 'Date' column to datetime and set as index
                data['Date'] = pd.to_datetime(data['Date'])
                data.set_index('Date', inplace=True)
            else:
                raise ValueError("Data must include a 'Date' column to set as a DatetimeIndex.")
        
        return data

    def get_returns(self, cfg, prices_data):
        """
        Process historical price data to calculate returns.
        """
        prices_data = prices_data.copy()
        prices_data['daily_returns'] = ffn.to_returns(prices_data['Close'])
        prices_data['monthly_returns'] = ffn.to_monthly(prices_data['Close']).to_returns()

        #TODO - Add more return calculations
        # - monthly_returns 
        # - visualize the data

        return prices_data
        
        