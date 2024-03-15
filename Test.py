import numpy as np
import pandas as pd
from KLSEScraping import KLSE

klse = KLSE("1155")

test = klse.scrap_stock_web_page()

test2 = klse.get_stock_basic_info()

print(klse.get_annual_financial_data())