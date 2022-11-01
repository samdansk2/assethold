'''
#TODO 
# a/ ?
'''

from data import AttributeDict
from finance_components import FinanceComponents

cfg_sec = {
    'filing_type': '4',
    'num_filings_to_download': 10,
    'include_amends': False,
    'after_date': None,
    'before_date': None
}
cfg = AttributeDict({
    "stocks": [{
        "ticker": "XOM"
    }],
    "source": "yfinance",
    "cfg_sec": cfg_sec
})

fc = FinanceComponents(cfg)
fc.fdata.get_data()
stock_data_dict = fc.get_data_dict()

fc.perform_analysis(stock_data_dict)
fc.dashboard()

print("debugging")