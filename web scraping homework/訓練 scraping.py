import time
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def product(keyword):


    # 設定 Chrome 瀏覽器的選項
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")   # 啟動時最大化
    options.add_argument("--incognito")         # 無痕模式
    options.add_argument("--disable-popup-blocking")  # 停用彈窗阻擋

    # 建立 Chrome 瀏覽器物件
    driver = webdriver.Chrome(options=options)
    driver.get("https://24h.pchome.com.tw/")

    driver.find_element(By.CSS_SELECTOR, ".o-iconFonts.o-iconFonts--actionClose").click()

    driver.find_element(By.CLASS_NAME,"c-search__input").send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR,".btn__square.btn__square--primary").click()

    all_phone_info=[]
    page = 1

    while True:
        time.sleep(2)

        item_list = driver.find_elements(By.CSS_SELECTOR,".c-prodInfoV2__title")
        price = driver.find_elements(By.CSS_SELECTOR,".c-prodInfoV2__priceValue.c-prodInfoV2__priceValue--m")
        link = driver.find_elements(By.CSS_SELECTOR,  ".c-prodInfoV2__link.gtmClickV2")
        img = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__img img")
        empty = driver.find_elements(
            By.CSS_SELECTOR,
            ".c-tipsBox__textFrame.c-tipsBox__textFrame--searchTipsBox"
        )

        if(empty or len(item_list) == 0) and page == 1:
            print("無此商品")
            driver.quit()
            return "無此商品"
        
        print(f"第{page}頁:商品數量{len(item_list)}")

        for name, price, buy, img in zip(item_list,price,link,img):
            name_text=  name.text.strip()
            price_text = price.text.strip()
            buy_href = buy.get_attribute("href")
            img_src = img.get_attribute("src")

                
            all_phone_info.append({
                "name":name_text,
                "price":price_text,
                "link":buy_href,
                "img":img_src
            })


        try:
            next_page_num = page +1 

            next_link=driver.find_element(
                By.XPATH,
                f"//ul[contains(@class,'c-pagination__pagesBar')]//a[text()='{next_page_num}']"
            )

            driver.execute_script("arguments[0].click();",next_link)
            page += 1

        except Exception:
            print("already the last page")
            break
    driver.quit() 

    for info in all_phone_info:
        print("name:",info["name"])
        print("price:",info["price"])
        print("link:",info["link"])
        print("img:",info["img"])
        print("-"*200)

    return all_phone_info
    
data = product("電腦")

with open("資訊.json","w",encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False,indent=4)