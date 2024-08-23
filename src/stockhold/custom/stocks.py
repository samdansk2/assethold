# Reader imports
from stockhold.analysis.stock_analysis import StockAnalysis
from stockhold.data.get_stock_data import GetStockData

stk_data = GetStockData(cfg=None)
stk_analysis = StockAnalysis(cfg=None)

class Stocks:
    
    def __init__(self):
        pass
    
    def router(self, cfg):
        #TODO add router logic
        cfg, data = stk_data.get_data(cfg)
        if cfg['analysis']['flag']:
            cfg = stk_analysis.router(cfg, stock_data)

