import time
from selenium import webdriver
from selenium.webdriver import ChromeService
from selenium.webdriver.common.by import By
import csv
import re
import random
from put_files_in_one import merge_file

service = ChromeService('./chromedriver/chromedriver.exe')
driver = webdriver.Chrome(service=service)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
    })
    """
})
driver.get('https://www.themarshallproject.org/next-to-die/al')
driver.implicitly_wait(15)

name = []
date = []
state = []
story = []
num = 1

state_list = driver.find_elements(By.CSS_SELECTOR, 'body > div.dp-container.dp-dark > div.dp-header > div.dp-menu > ul > li')
for i in range(1, len(state_list)-3):
    label = driver.find_element(By.CSS_SELECTOR, f'body > div.dp-container.dp-dark > div.dp-header > div.dp-menu > ul > li:nth-child({i}) > a')
    label.click()
    # time.sleep(0.5)
    name = driver.find_elements(By.CSS_SELECTOR, 'li.dp-previous-name a')
    for j in range(len(name)):
        href = name[j].get_attribute('href')
        driver.get(href)
        rnd_time1 = random.uniform(0.4, 0.6)
        time.sleep(rnd_time1)
        name_d = driver.find_element(By.CSS_SELECTOR, '#name_0').text
        date_d = driver.find_element(By.CSS_SELECTOR, '#name_0_time').text
        state_d = driver.find_element(By.CSS_SELECTOR, '#dp-case-state').text
        name.append(name_d)
        date.append(date_d)
        state.append(date_d)
        try:
            story_d = driver.find_element(By.CSS_SELECTOR, '#dp-case-summary-lede').text
            story_d.strip()
            pattern = r" READ MORE ↓"
            story_d = re.sub(pattern, '', story_d)
        except:
            story_d = ''
        # print(story_d)
        # print('-----------')
        # print(name_d)
        # print('-----------')
        # print(date_d)
        # print('-----------')
        # print(state_d)
        # print('-----------')
        # print(href)
        file_path = './data/' + f'{state_d}.csv'
        # print(file_path)
        with open(file_path, mode='a', encoding='utf-8', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow([name_d, date_d, state_d, story_d, href])
        driver.back()
        print(f"Quantity completed:{num}")
        num = num + 1
        rnd_time2 = random.uniform(0.4, 0.6)
        time.sleep(rnd_time2)
    #     break
    # break
driver.quit()

merge_file()
