# Third party imports
import pandas as pd # noqa

class Portfolio():
    
    def __init__(self, cfg):

        self.cfg = cfg

    def router(self, cfg):

        self.portfolio_value(cfg)
        return cfg
    
    def portfolio_value(self, cfg):

        #TODO dividends need to be formatted and read
        data_format = 'fidelity'
        file_path = cfg['portfolio']['transaction_csv']

        expected_columns = ['Run Date', 'Account', 'Action', 'Symbol', 'Description', 'Type', 'Quantity', 'Price ($)', 'Commission ($)', 'Fees ($)', 'Accrued Interest ($)', 'Amount ($)', 'Settlement Date']

        # Read the CSV file, ignoring rows with more than 13 columns
        df = pd.read_csv(file_path, usecols=range(13), names=expected_columns, header=0, on_bad_lines='skip')

        df['Run Date'] = pd.to_datetime(df['Run Date'])

        df['Amount ($)'] = pd.to_numeric(df['Amount ($)'], errors='coerce').fillna(0) # Convert to numeric, fill NaN with 0

        accounts = df['Account'].unique()
        account_dfs = {account: df[df['Account'] == account] for account in accounts}

        print(account_dfs)

        # Cumulative value by account
        cumulative_values = {}
        for account, account_df in account_dfs.items():
            cumulative_values[account] = account_df['Amount ($)'].sum()

        print(cumulative_values)

        # Cumulative value by symbol
        cumulative_values = {}
        for account, account_df in account_dfs.items():
            symbols = account_df['Symbol'].unique()
            symbol_dfs = {symbol: account_df[account_df['Symbol'] == symbol] for symbol in symbols}
            cumulative_values[account] = {symbol: symbol_df['Amount ($)'].sum() for symbol, symbol_df in symbol_dfs.items()}

        print(cumulative_values)




        
        
