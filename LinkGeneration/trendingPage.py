import selenium
import csv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
import time

options = ChromeOptions()
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.youtube.com/feed/trending")

data = driver.find_elements_by_xpath('//*[@id="thumbnail"]')
links = []

for i in data:
    links.append(i.get_attribute('href'))

with open("trending_links.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(links)

driver.quit()
