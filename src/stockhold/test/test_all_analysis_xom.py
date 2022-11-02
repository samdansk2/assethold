from stockhold import stock_analysis
from stockhold.common.data import AttributeDict

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
    "cfg_sec": cfg_sec,
    "dashboard": True
})

stock_analysis.stock_analysis(cfg)
