import pandas as pd #noqa
import yaml #noqa
import numpy as np #noqa
import os #noqa

class Portfolio:
    
    def __init__(self, cfg):
        self.cfg = cfg

    def router(self, cfg):

        csv_folder = r"src\assethold\tests\test_data\analysis\Portfolio\results\Data" 
        os.makedirs(csv_folder, exist_ok=True)  

        all_years_by_account = {}
        all_years_by_symbol = {}

        years_data = cfg['portfolio']
        for key, file_path in years_data.items():
            year = file_path.split('/')[-1].split('.')[0]  # Extract year from file name
            yearly_data = self.portfolio_value(file_path)

            for account, value in yearly_data['by_account'].items():
                if account not in all_years_by_account:
                    all_years_by_account[account] = {}
                all_years_by_account[account][year] = value

            for symbol, value in yearly_data['by_symbol'].items():
                if symbol not in all_years_by_symbol:
                    all_years_by_symbol[symbol] = {}
                all_years_by_symbol[symbol][year] = value
        
        by_account_path = os.path.join(csv_folder, "by_account.txt")
        by_symbol_path = os.path.join(csv_folder, "by_symbol.txt")

        with open(by_account_path, "w") as f:
            f.write("Account-wise Cumulative Values by Year:\n")
            for account, years in all_years_by_account.items():
                f.write(f"\nAccount: {account}\n")
                for year, value in years.items():
                    f.write(f"  {year}: {value}\n")


        with open(by_symbol_path, "w") as f:
            f.write("Symbol-wise Cumulative Values by Year:\n")
            for symbol, years in all_years_by_symbol.items():
                f.write(f"\nSymbol: {symbol}\n")
                for year, value in years.items():
                    f.write(f"  {year}: {value}\n")

        print(f"****Cumulative values for each year have been saved successfully.****")
        print()

        return cfg

    def portfolio_value(self, file_path):

        expected_columns = [
            'Run Date', 'Account', 'Action', 'Symbol', 'Description', 'Type',
            'Quantity', 'Price ($)', 'Commission ($)', 'Fees ($)', 
            'Accrued Interest ($)', 'Amount ($)', 'Settlement Date'
        ]

        df = pd.read_csv(file_path, usecols=range(13), names=expected_columns, header=0, on_bad_lines='skip')

        df['Run Date'] = pd.to_datetime(df['Run Date'])
        df['Amount ($)'] = pd.to_numeric(df['Amount ($)'], errors='coerce').fillna(0)
        df['Symbol'] = df['Symbol'].str.strip()
        df['Symbol'] = df['Symbol'].replace('', np.nan) # replace empty strings with NaN
        df['Account'] = df['Account'].str.strip()

        #  replace missing 'Symbol' with 'cash'
        mask_individual = (df['Account'] == 'Individual X78707567') & df['Symbol'].isna() & df['Action'].str.contains('cash', case=False, na=False)
        df.loc[mask_individual, 'Symbol'] = 'cash'

        mask_individual = (df['Account'] == 'Traditional IRA 224886419') & df['Symbol'].isna() & df['Action'].str.contains('cash', case=False, na=False)
        df.loc[mask_individual, 'Symbol'] = 'cash'

        cencora_acc = (df['Account'] == 'CENCORA 82897') & df['Symbol'].isna() 
        df.loc[cencora_acc, 'Symbol'] = df.loc[cencora_acc, 'Description']

        accounts = df['Account'].unique()
        account_dfs = {account: df[df['Account'] == account] for account in accounts}

        # Cumulative metrics by account
        cumulative_by_account = {}
        for account, account_df in account_dfs.items():
            cumulative_by_account[account] = account_df['Amount ($)'].sum()

        cumulative_by_symbol = {}
        for account, account_df in account_dfs.items():
            symbols = account_df['Symbol'].unique()
            symbol_dfs = {symbol: account_df[account_df['Symbol'] == symbol] for symbol in symbols}
            cumulative_by_symbol[account] = {symbol: symbol_df['Amount ($)'].sum() for symbol, symbol_df in symbol_dfs.items()}

        return {'by_account': cumulative_by_account, 'by_symbol': cumulative_by_symbol}
