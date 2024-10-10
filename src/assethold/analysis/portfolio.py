class Portfolio():
    '''
    cash in or cash out, dividend payout. 
    value of portfolio. dercerase in asset value
    
    if you are depositing cash in to the account, then this increases. 1 month 1000
    if you are withdrawing cash from the account, then this decreases. 1 month -1000
    
    if a stock pays dividend, add dividend to the cash value.
    if a stock is sold, then add the value of the stock to the cash value.
    
    '''
    def __init__(self, cfg):
        self.cfg = cfg
        self.cash = 10000  # Example starting cash
        self.holdings = 0
        self.transactions = []  
    
    def router(self, cfg):
        pass
    def calculation(self, cfg, daily_data, breakout_daily_data_trend_df):
        pass
        
