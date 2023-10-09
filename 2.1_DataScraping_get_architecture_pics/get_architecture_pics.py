import time
from selenium import webdriver
from selenium.webdriver import ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import requests
import parsel
import os


service = ChromeService(executable_path=r"chromedriver\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get("https://www.archdaily.com")
driver.implicitly_wait(10)
# driver.maximize_window()  #DON'T RUN THIS !!!!
input_tag = driver.find_element(By.XPATH, '//*[@id="afd-search-actions-mobile"]/div/input')
input_tag.send_keys('tiny house')
input_tag.send_keys(Keys.ENTER)

js_all = 'document.documentElement.scrollTop=document.documentElement.scrollHeight'
driver.execute_script(js_all)
for i in range(1, 40, 2):  # 1,3,5,7,9 控制下拉的次数
    time.sleep(1)
    j = i / 39
    js_all2 = 'document.documentElement.scrollTop=document.documentElement.scrollHeight * %f' % j
    driver.execute_script(js_all)

label_list = driver.find_elements(By.XPATH,'/html/body/div[5]/div/div[2]/div/div/div/a')
print(len(label_list))
# print(label_list)
for label in label_list:
    try:
        href = label.get_attribute('href')
        print(href)
        title_architect = label.find_element(By.CSS_SELECTOR,'a > h3').text
        title_architect = title_architect.split('/')
        title = title_architect[0].strip()
        architect = title_architect[1].strip()
        html = requests.get(href)  #into_web
        selector = parsel.Selector(html.text)
        # print(selector)
        # driver.get(href)
        label_list2 = selector.css('figure.js-image-size').getall()  #find_figure
        # labels_list2 = driver.find_elements(By.CSS_SELECTOR,'figure.js-image-size')
        # print(label_list2)
        dir_name = title + '_' + architect
        path = f"./Archdaily_pics/{dir_name}"
        os.makedirs(path,exist_ok=True)

        num = 1

        for label2 in label_list2:
            # try:
            selector2 = parsel.Selector(label2)
            img_url =selector2.css('figure a picture img::attr(src)').get()  #获取图片url
            # img_url = label2.find_element(By.CSS_SELECTOR,'figure a picture img').get_attribute('src')
            img = requests.get(img_url)
            with open(f'./Archdaily_pics/{dir_name}/{num}.jpg', mode='wb') as f:
                f.write(img.content)
            print(f'Number of downloads:{num}')
            num += 1
    except:
        pass
    # break



input('please press ENTER to quit:')
driver.quit()