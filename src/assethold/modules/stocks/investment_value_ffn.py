import ffn
import pandas as pd
import matplotlib.pyplot as plt

class InvestmentValueFfn:

    def __init__(self):
        pass

    def router(self, cfg, holdings_df):

        prices_data = self.prepare_data(holdings_df)
        self.get_daily_returns(cfg, prices_data)
        self.get_monthly_returns(cfg, prices_data)

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

    def get_daily_returns(self, cfg, prices_data):
      
        prices_data = prices_data.copy()
        prices_data['daily_returns'] = ffn.to_returns(prices_data['Close'])
        self.save_results(prices_data, 'ffn_daily_returns.csv')

        return prices_data
    
    def get_monthly_returns(self, cfg, prices_data):
     
        prices_data = prices_data.copy()
        prices_data.sort_index(inplace=True)  # Ensure data is sorted
        prices_data = prices_data[~prices_data.index.duplicated()] 

        monthly_prices = prices_data['Close'].resample('ME').last()
        monthly_returns = monthly_prices.pct_change()

        prices_data['monthly_returns'] = monthly_returns
        self.save_results(prices_data, 'ffn_monthly_returns.csv')
        return prices_data
    
    def save_results(self, prices_data,file_name):
        csv_path = r'tests\modules\stocks\analysis\investment\results\Data'
        prices_data.to_csv(f'{csv_path}\\{file_name}', index=True)

       
        
        