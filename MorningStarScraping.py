from selenium import webdriver
import time

cService = webdriver.ChromeService(executable_path='C:\\Users\\OON YEE SEM\\Documents\\Developer\\Chrome Driver\\chromedriver.exe')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--incognito')
browser = webdriver.Chrome(service = cService,options = chrome_options)
browser.get("https://www.morningstar.com/stocks/xkls/5196/Valuation")

time.sleep(2)

element = browser.find_element("class","sal-component-title-h2")
print(element)