from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

cService = webdriver.ChromeService(executable_path='C:\\Users\\OON YEE SEM\\Documents\\Developer\\Chrome Driver\\chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
browser = webdriver.Chrome(service = cService,options = chrome_options)
# browser.get("https://www.morningstar.com/stocks/xkls/5196/Valuation")

# # time.sleep(15)
# WebDriverWait(browser,5).until(
#     EC.presence_of_element_located((By.CSS_SELECTOR, ".mds-td__sal"))
# )

# elements = browser.find_elements(By.CSS_SELECTOR, ".mds-td__sal")
# scarp_key_statistics_data = [element.text.strip() for element in elements]

# PB_index = scarp_key_statistics_data.index("Price/Book")
# stop_index = scarp_key_statistics_data.index("Price/Forward Earnings")

# PB = scarp_key_statistics_data[PB_index:stop_index][:-3]

# # Find the table element containing the years
# table = browser.find_element(By.XPATH,"//table")
# headers = table.find_elements(By.XPATH,".//th[contains(@class, 'mds-th__sal')]")
# years = [year.text.strip() for year in headers[1:]][:-3]


# print(PB)
# print(years)

browser.get("https://www.morningstar.com/stocks/xkls/5196/Financials")
time.sleep(5)

link = browser.find_element(By.XPATH,'//*[@id="__layout"]/div/div/div[2]/div[3]/section/div[2]/main/div[2]/div/div/div/div[1]/sal-components/div/sal-components-stocks-financials/div/div/div/div/div/div/div[2]/div[2]/div/div/a')
link.click()

time.sleep(10)

elements = browser.find_elements(By.CSS_SELECTOR, ".tg-header-column")
elements = [item.text.strip() for item in elements]
print(elements)

#browser.quit()


