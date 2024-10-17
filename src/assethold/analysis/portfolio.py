class Portfolio():
    '''
    Objective: Calculate value of a single or group of assets over time.

    cash in or cash out, dividend payout. 
    value of portfolio. dercerase in asset value
    
    if you are depositing cash in to the account, then this increases. 1 month 1000
    if you are withdrawing cash from the account, then this decreases. 1 month -1000
    
    if a stock pays dividend, add dividend to the cash value.
    if a stock is sold, then add the value of the stock to the cash value.

    Green : Currency 1000 buy next trading day every week.
    Gold: 200 position sell next trading day every week till reaching 50% portofolio.
    Red: 500 position sell next trading day every week till reaching 20% portofolio.

    Track/plot total portoflio value, cash value, stock value , profit etc. every day.
    
    '''
    def __init__(self, cfg):
        self.cfg = cfg
        self.cash = 10000  # initial cash
        self.stock_value = 0 # initial stock value
        self.holdings = 0 # number of stocks
        self.portfolio_history = []  
    def router(self, cfg):

        self.portfolio_value(cfg)
        return cfg
    
    def portfolio_value(self, cfg):
        cfg_portfolio = cfg['portfolio']
        portfolio_value = 0
        transactions = cfg_portfolio['transactions']
        for transaction in transactions:
            cash = self.get_transation_cash(transaction)
            portfolio_value += cash 

        print(portfolio_value)


    def get_transation_cash(self, transaction):
        cash = 0
        if 'cash' in transaction:
            cash = transaction['cash']
        return cash

    def get_stock_value(self, transaction):
        #     stock_price = row['Close'] 
        pass

        # for i, row in breakout_daily_data_trend_df.iterrows():
        #     breakout_color = row['plot_color'] 

        #     if breakout_color == 'green':
        #         # buy stocks
        #         pass
        #     elif breakout_color == 'gold':
        #         # sell stocks
        #         pass
        #     elif breakout_color == 'red':
        #         # sell stocks
        #         pass



        
        
