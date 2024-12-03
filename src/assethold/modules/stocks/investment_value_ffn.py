import ffn
import pandas as pd
import matplotlib.pyplot as plt

class InvestmentValueFfn:

    def __init__(self):
        pass

    def router(self, cfg, prices_data):

        prices_data = self.prepare_data(prices_data)
        data = self.get_daily_returns(cfg, prices_data)
        data = self.get_monthly_returns(cfg, prices_data)

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
        returns = ffn.to_log_returns(prices_data['Close'])
        prices_data['daily_returns'] = returns

        self.plot_returns(returns, prices_data)
        self.save_results(prices_data, 'ffn_daily_returns.csv')

        return prices_data
    
    def get_monthly_returns(self, cfg, prices_data):
     
        prices_data = prices_data.copy()
        prices_data.sort_index(inplace=True)  # Ensure data is sorted
        prices_data = prices_data[~prices_data.index.duplicated()] 

        stats = prices_data['Close'].calc_stats()

        monthly_returns = stats.return_table

        self.save_results(monthly_returns, 'ffn_monthly_returns.csv')

        return monthly_returns
    
    def plot_returns(self, daily_returns, prices_data):
        
        import matplotlib.dates as mdates #noqa

        daily_returns = daily_returns.dropna()
        daily_returns = daily_returns[:100]
        fig, ax = plt.subplots(figsize=(12, 6))
        
        plt.plot(daily_returns.index, daily_returns, label=' Returns', color='green')
        plt.title('Daily Returns', fontsize=16)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Returns', fontsize=12)
        plt.legend()
        ax.grid(True)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

        plt.savefig('tests/modules/stocks/analysis/investment/results/Plot/daily_returns.png')
    
    def save_results(self, prices_data,file_name):

        csv_path = r'tests\modules\stocks\analysis\investment\results\Data'
        prices_data.to_csv(f'{csv_path}\\{file_name}', index=True)



       
        
        