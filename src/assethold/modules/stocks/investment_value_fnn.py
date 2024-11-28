import ffn
import pandas as pd
import matplotlib.pyplot as plt

class InvestmentValueFnn:

    def __init__(self):
        pass

    def router(self, cfg, holdings_df):

        prices_data = self.prepare_data(holdings_df)
        self.get_returns(cfg, prices_data)

        return cfg, prices_data

    def get_returns(self, cfg, prices_data):
        """
        Process historical price data to calculate returns.
        """
        prices_data = prices_data.copy()
        returns = ffn.to_returns(prices_data)
        
        ax = returns.hist(figsize=(12, 5))
        # plt.show()
        
        ax = prices_data.rebase().plot(figsize=(12,5))
        #plt.show()

        perf = prices_data.calc_stats()
        
    def prepare_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepare data for analysis by ensuring the index is a DatetimeIndex.
        """
        if not isinstance(data.index, pd.DatetimeIndex):
            if 'Date' in data.columns:
                # Convert 'Date' column to datetime and set as index
                data['Date'] = pd.to_datetime(data['Date'])
                data.set_index('Date', inplace=True)
            else:
                raise ValueError("Data must include a 'Date' column to set as a DatetimeIndex.")
        
        return data
        
        
        