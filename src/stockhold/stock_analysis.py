from stockhold.common.data import AttributeDict
from stockhold.finance_components import FinanceComponents


def stock_analysis(ticker, dashboard_flag=True):
    cfg = get_detailed_cfg(ticker, dashboard_flag)
    fc = FinanceComponents(cfg)

    fc.fdata.get_data()
    stock_data_dict = fc.get_data_dict()
    fc.perform_analysis(stock_data_dict)

    if cfg['dashboard']:
        fc.dashboard()


def get_detailed_cfg(ticker, dashboard_flag):
    cfg = AttributeDict({
        "stocks": [{
            "ticker": ticker
        }],
        "dashboard": dashboard_flag,
        "source": "yfinance"
    })

    cfg_sec = {
        'filing_type': '4',
        'num_filings_to_download': 10,
        'include_amends': False,
        'after_date': None,
        'before_date': None
    }
    cfg.update({"cfg_sec": cfg_sec})

    return cfg