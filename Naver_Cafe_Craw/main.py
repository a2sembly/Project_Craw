from crawl import *
from settings import *
import time

print(WEB_DRIVER_PATH)
driver = webdriver.Chrome(WEB_DRIVER_PATH)
index = 0
login_naver(naver_id,naver_pw,driver)
time.sleep(1)
save_tweet_data_to_csv(None, XLSX_PATH, 'w')  # create file for saving records
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME):
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    cafe_posting_urls = get_cafe_posting_urls(dining_name, start_date, end_date, driver)
    print(start_date, end_date, dining_name)
    # cafe_postings의 date, text, title 가져오기
    total_list = []

    for posting_addr in cafe_posting_urls:
        date = get_element(DATE, posting_addr, driver)

        text = get_element(TEXT, posting_addr, driver)

        title = get_element(TITLE, posting_addr, driver)

        comment = get_element(COMMENT, posting_addr, driver)

        total_list.append([date,title,text,comment])

    save_tweet_data_to_csv(total_list, XLSX_PATH)
