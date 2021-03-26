from crawl import *
from settings import *
import time

driver = webdriver.Chrome(WEB_DRIVER_PATH)
index = 0
time.sleep(1)
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME,):
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    Twitter_posting_urls = get_twitter_postings(dining_name, start_date, end_date, driver, XLSX_PATH)
    print(start_date, end_date, dining_name)
    # Twitter_postings의 date, text, title 가져오기

