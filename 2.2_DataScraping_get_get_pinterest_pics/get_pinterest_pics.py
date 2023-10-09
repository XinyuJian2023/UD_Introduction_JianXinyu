import time
from selenium import webdriver
from selenium.webdriver import ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import os

service = ChromeService(executable_path=r"chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
    "source":"""
    Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
    })
    """
})
driver.implicitly_wait(10)
url="https://www.pinterest.com/PinterestUK/"
driver.maximize_window()
time.sleep(2)
driver.get(url)
search_query = driver.find_element("name", "q")
search_query.send_keys("Rem Koolhaas")
search_query.send_keys(Keys.RETURN)
time.sleep(1)

js_all = 'document.documentElement.scrollTop=document.documentElement.scrollHeight'
driver.execute_script(js_all)
for i in range(1, 20, 2):
    time.sleep(1)
    j = i / 19
    js_all2 = 'document.documentElement.scrollTop=document.documentElement.scrollHeight * %f' % j
    driver.execute_script(js_all)

articles = driver.find_elements(By.CSS_SELECTOR, "img.hCL.kVc.L4E.MIw")
num = 1
print(len(articles))
for i in articles:
    try:
        src = i.get_attribute('src')
        print(src)
        path = f"./pinterest_pics"
        os.makedirs(path,exist_ok=True)
        img = requests.get(src)
        with open(f"./pinterest_pics/{num}.jpg",mode='wb') as f:
            f.write(img.content)
        num += 1
    except:
        pass
driver.quit()


