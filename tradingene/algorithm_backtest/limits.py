from datetime import datetime

################################################################################
#                               SLIPPAGEs constants
################################################################################
BTCUSD_SLIPPAGE = 1e0
ETHUSD_SLIPPAGE = 1e-1
LTCUSD_SLIPPAGE = 1e-2
ETHBTC_SLIPPAGE = 1e-6
LTCBTC_SLIPPAGE = 1e-6
DSHBTC_SLIPPAGE = 1e-6
XRPBTC_SLIPPAGE = 1e-9
EOSUSD_SLIPPAGE = 1e-4
EOSBTC_SLIPPAGE = 1e-6
XBTUSD_SLIPPAGE = 1e-1
SI_SLIPPAGE = 1e0
RTS_SLIPPAGE = 1e0
BR_SLIPPAGE = 1e-2
SBRF_SLIPPAGE = 1e0
GAZR_SLIPPAGE = 1e0
################################################################################

################################################################################
#                               Data constants
################################################################################
LOOKBACK_PERIOD = 150
################################################################################

################################################################################
#                               Backtest constants
################################################################################
EARLISET_START = datetime(2017, 1, 1)
MAX_AVAILABLE_VOLUME = 1

################################################################################
#                               Instrument's IDs
################################################################################
instrument_ids = {
    'btcusd': 18,
    'ethusd': 19,
    'ltcusd': 20,
    'ethbtc': 22,
    'ltcbtc': 23,
    'dshbtc': 24,
    'xrpbtc': 25,
    'eosusd': 26,
    'eosbtc': 27,
    'xbtusd': 28,
    'si': 42,
    'rts': 43,
    'br': 44,
    'sbrf': 45,
    'gazr': 46
}

################################################################################
#                               MOEX Tickers
################################################################################
moex_tickers = [
    'si', 'rts', 'br', 'sbrf', 'gazr'
]