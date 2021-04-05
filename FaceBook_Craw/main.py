from crawl import *
from settings import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

total_list = []
title_list = []
date_list = []
option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
driver = webdriver.Chrome(chrome_options=option, executable_path=WEB_DRIVER_PATH)
index = 0
PAGE_COUNT = 0
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME,):
    alert("[+] Craw Start!")
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    Facebook_posting = Facebook_postings_urls(dining_name, start_date, end_date, driver, title_list,date_list)
    print(start_date, end_date, dining_name)
    # blog_postings의 date, text, title 가져오기

    for posting_addr,title in zip(Facebook_posting, title_list):
        alert("[+] Get Posting Data")
        date = get_element(DATE, posting_addr, driver,PAGE_COUNT)
        PAGE_COUNT = 1
        text = get_element(TEXT, posting_addr, driver,PAGE_COUNT)
        PAGE_COUNT = 0
        
        total_list.append([date,title,text])

    driver.quit()
    save_tweet_data_to_csv(total_list, XLSX_PATH)
    alert("[+] Exit")
