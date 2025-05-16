"""
pip install selenium webdriver_manager 下載套件
pip uninstall selenium webdriver_manager 刪除套件
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

#%% 範例一: 模擬搜尋 
# 定義抓取一頁資料的函數
def extract_page_data():
    time.sleep(1)
    items = driver.find_elements(By.CSS_SELECTOR,".result-item") # 收尋化石的資料
    for item in items:
        title_element = item.find_element(By.TAG_NAME, "a") # Q?
        title = title_element.text
        link = title_element.get_attribute("href")
        data_list.append({"標題": title, "連結": link})
        print(title, link)


#%%
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
    options=options
)
# 啟動瀏覽器
driver.get("https://www.nmns.edu.tw/ch/")
driver.maximize_window()

# 搜尋關鍵字

search_box = driver.find_element(By.CLASS_NAME, "search") #搜尋『全站收尋』
driver.execute_script("arguments[0].click();", search_box) # 用 JS 模擬點擊避免動畫干擾
time.sleep(3)
search_box = driver.find_element(By.ID, "headerSearchKeyword") # 收尋 『請輸入關鍵字』
driver.execute_script("arguments[0].click();", search_box)
search_box.send_keys("化石")
time.sleep(2)
search_box.send_keys(Keys.ENTER)


#time.sleep(2)

# 存放所有資料的列表
data_list = []

# 迴圈抓多頁
count=0
while count<3:
    time.sleep(2)
    extract_page_data()
    try:
        next_button = driver.find_element(By.CSS_SELECTOR,'button[aria-label = "Next page"]') # Q?
        if next_button.is_enabled():
            next_button.click()
        else:
            break  # 已經是最後一頁
    except (NoSuchElementException, ElementNotInteractableException):
        break
    count +=1
    #time.sleep(2)

driver.quit()


#%%
import pandas as pd
# 轉為 DataFrame 並輸出成 CSV
df = pd.DataFrame(data_list)
df.to_csv(r"Users\zhangjianxiang\爬蟲結果\2025_5_8化石data.csv", index=False, encoding="utf-8-sig")







