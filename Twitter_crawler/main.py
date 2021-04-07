from crawl import *
from settings import *
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

option = Options()
option.add_argument("headless")
option.add_argument("--disable-gpu")
option.add_argument("lang=ko_KR")
option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
driver = webdriver.Chrome(chrome_options=option, executable_path=WEB_DRIVER_PATH)
index = 0
time.sleep(1)
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME,):
    alert("[+] Craw Start!")
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    Twitter_posting_urls = get_twitter_postings(dining_name, start_date, end_date, driver, XLSX_PATH)
    # Twitter_postings의 date, text, title 가져오기
    alert("[+] Exit")
