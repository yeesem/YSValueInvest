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
browser.get("https://www.google.com")

WebDriverWait(browser,5).until(
    EC.presence_of_element_located((By.CLASS_NAME,"gLFyf"))
)

input_element = browser.find_element(By.CLASS_NAME,"gLFyf")
input_element.clear()
input_element.send_keys("tech with tim" + Keys.ENTER)

WebDriverWait(browser,5).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT,"Tech With Tim"))
)

#By.LINK_TEXT - use to find the exact tag
#By.PARTIAL_LINK_TEXT - use to find if text is contained inside an anchor text
#If we want to find all the links that had "Tech with Tim" - use element's'
#will return an array of all different elements
link = browser.find_element(By.PARTIAL_LINK_TEXT,"Tech With Tim")
link.click()

time.sleep(2)

browser.quit()