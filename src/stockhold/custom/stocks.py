# Reader imports
from stockhold.analysis.stock_analysis import StockAnalysis
from stockhold.data.get_stock_data import GetStockData

stk_data = GetStockData(cfg=None)
stk_analysis = StockAnalysis(cfg=None)

class Stocks:
    
    def __init__(self):
        pass
    
    def router(self, cfg):

        cfg, data =  stk_data.router(cfg)
        cfg, analysis = stk_analysis.router(cfg, data)

        return cfg
