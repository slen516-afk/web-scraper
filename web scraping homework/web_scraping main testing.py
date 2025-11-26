import time
import json
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def product(keyword):
    service = Service('./chromedriver.exe')

    # 設定 Chrome 瀏覽器的選項
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")   # 啟動時最大化
    options.add_argument("--incognito")         # 無痕模式
    options.add_argument("--disable-popup-blocking")  # 停用彈窗阻擋

    # 建立 Chrome 瀏覽器物件
    driver = webdriver.Chrome(options=options)
    driver.get("https://24h.pchome.com.tw/")

    # 關掉一開始的廣告
    driver.find_element(By.CSS_SELECTOR, ".o-iconFonts.o-iconFonts--actionClose").click()

    # 搜尋關鍵字
    driver.find_element(By.CLASS_NAME, "c-search__input").send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, ".btn__square.btn__square--primary").click()

    all_phone_info = []
    page = 1  # 目前在第幾頁

    while True:
        time.sleep(2)  # 等這一頁的商品載入完

        # 每一頁都要重新抓一次元素（翻頁後舊的 element 會失效）
        phone_list = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__title")
        phone_price = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__priceValue.c-prodInfoV2__priceValue--m")
        buy_link = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__link.gtmClickV2")
        phone_img = driver.find_elements(By.CSS_SELECTOR, ".c-prodInfoV2__img img")
        empty = driver.find_elements(
            By.CSS_SELECTOR,
            ".c-tipsBox__textFrame.c-tipsBox__textFrame--searchTipsBox"
        )

        # 第一頁就沒有商品 → 可以直接結束
        if (empty or len(phone_list) == 0) and page == 1:
            print("無此商品")
            driver.quit()
            return "無此商品"

        print(f"第 {page} 頁：商品數量 {len(phone_list)}")

        # 收集這一頁的資料
        for name_el, price_el, buy_el, img_el in zip(phone_list, phone_price, buy_link, phone_img):
            name_text = name_el.text.strip()
            price_text = price_el.text.strip()
            buy_href = buy_el.get_attribute("href")
            img_src = img_el.get_attribute("src")

            all_phone_info.append({
                "name": name_text,
                "price": price_text,
                "link": buy_href,
                "img": img_src
            })

        # ===== 準備翻到下一頁 =====
        try:
            next_page_num = page + 1
            # 在分頁列裡面找文字剛好是「下一個頁碼」的連結
            next_link = driver.find_element(
                By.XPATH,
                f"//ul[contains(@class,'c-pagination__pagesBar')]//a[text()='{next_page_num}']"
            )

            # 找得到就點下一頁
            driver.execute_script("arguments[0].click();", next_link)
            page += 1
        except Exception:
            # 找不到下一個頁碼的連結 → 已經是最後一頁，結束迴圈
            print("已經到最後一頁")
            break

    # 全部頁面都抓完再關掉瀏覽器
    driver.quit()

    # 印出確認
    for info in all_phone_info:
        print("name:", info["name"])
        print("price:", info["price"])
        print("link:", info["link"])
        print("img:", info["img"])
        print("-" * 120)

    return all_phone_info


data = product("飛機杯")

with open("product_info.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
