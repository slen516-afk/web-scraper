import time
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service



def product(keyword):
   
    service = Service('./chromedriver.exe')

# 設定 Chrome 瀏覽器的選項
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized") # Chrome 瀏覽器在啟動時最大化視窗 RWD響應式網頁設計
    options.add_argument("--incognito") # 無痕模式
    options.add_argument("--disable-popup-blocking") # 停用 Chrome 的彈窗阻擋功能。

# 建立 Chrome 瀏覽器物件

    driver = webdriver.Chrome(options=options)
    driver.get("https://24h.pchome.com.tw/")

# driver.quit() #關閉瀏覽器


    driver.find_element(By.CSS_SELECTOR,".o-iconFonts.o-iconFonts--actionClose").click()
    driver.find_element(By.CLASS_NAME,"c-search__input").send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR,".btn__square.btn__square--primary").click()

    phone_list = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__title")
    phone_price = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__priceValue.c-prodInfoV2__priceValue--m")
    buy_link = driver.find_elements(By.CSS_SELECTOR,".c-prodInfoV2__link.gtmClickV2")
    phone_img = driver.find_elements(By.CSS_SELECTOR,".c-prodInfoV2__img img")
    empty = driver.find_elements(By.CSS_SELECTOR,".c-tipsBox__textFrame.c-tipsBox__textFrame--searchTipsBox")


    if empty or len(phone_list) == 0:
        print("無此商品")
        driver.quit()
        return "無此商品"
    
    time.sleep(1)
    last_phone_price = phone_price[-1]
    last_link = buy_link[-1]
    last_img = phone_img[-1]
    # print(f"手機價格數量:{len(phone_price)}")
    last_phone = phone_list[-1] #如果上面的條件找不到就用模糊搜尋
    # print(f"目前數量:{len{phone_list}}")
    # print(f"手機數量:{len(phone_list)}")
    # print(f"連結數量:{len(buy_link)}")
    # print(f"圖片數:{len(phone_img)}")

    while True:

        if empty:
            print("No such product")
        
        if last_phone == phone_list[-1]:
            break
        last_phone = phone_list[-1]
        print(f"手機數量:{len(phone_list)},價格:{len(phone_price)}")

    all_phone_info = []

    for name, price, buy, img in zip(phone_list, phone_price, buy_link, phone_img):
        name = name.text.strip()
        price = price.text.strip()
        buy_link = buy.get_attribute("href")
        phone_img = img.get_attribute("src")

        all_phone_info.append({
            "name": name.strip(),
            "price": price.strip(),
            "link": buy_link,
            "img": phone_img

        })
    for info in all_phone_info:
        print("name:", info["name"])
        print("price:", info["price"])
        print("link:", info["link"])
        print("img:", info["img"])
        print("-" * 120)   
    return all_phone_info
        
data = product("手電筒")

with open("product_info.json", "w",encoding="utf-8")as f:
    json.dump(data, f,ensure_ascii=False, indent=4)


