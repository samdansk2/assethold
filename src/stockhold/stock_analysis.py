from stockhold.finance_components import FinanceComponents


def stock_analysis(cfg):
    fc = FinanceComponents(cfg)
    fc.fdata.get_data()
    stock_data_dict = fc.get_data_dict()

    fc.perform_analysis(stock_data_dict)
    if cfg['dashboard']:
        fc.dashboard()
