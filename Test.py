import numpy as np
import pandas as pd
from KLSEScraping import KLSE

klse = KLSE("1155")

test = klse.scrap_stock_web_page()

print(klse.get_quarter_financial_data())