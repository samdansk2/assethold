import ffn
import pandas as pd


class InvestmentValueFnn:

    def __init__(self):
        pass

    def router(self, cfg, ticker_data):
       
        return self.get_returns(cfg, ticker_data)

    def get_returns(self, cfg, ticker_data):
        """
        Process historical price data to calculate returns.
        """
        if not isinstance(ticker_data, pd.DataFrame):
            raise ValueError("ticker_data must be a pandas DataFrame.")

        ticker_data.set_index(pd.to_datetime(ticker_data.index), inplace=True)
        ticker_data = ffn.to_returns(ticker_data)
        daily_returns = ticker_data

        # Add daily returns column
        ticker_data["daily_returns"] = daily_returns

        # Resample to calculate monthly returns
        monthly_prices = ticker_data.resample("M").last()  # Get last price of each month
        monthly_returns = monthly_prices.to_returns().dropna()

        # Add monthly returns column (forward-fill to align with daily index)
        monthly_returns = monthly_returns.reindex(ticker_data.index, method="ffill")
        ticker_data["monthly_returns"] = monthly_returns

        return ticker_data

    
