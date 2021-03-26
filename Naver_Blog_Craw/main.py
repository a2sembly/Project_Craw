from crawl import *
from settings import *

print(WEB_DRIVER_PATH)
driver = webdriver.Chrome(WEB_DRIVER_PATH)
index = 0
PAGE_COUNT = 0
for start_date, end_date, dining_name in zip(START_DATE, END_DATE, DINING_NAME,):
    # 키워드, 검색 시작/종료 날짜의 포스팅 url을 가져오기
    blog_posting_urls = get_blog_posting_urls(dining_name, start_date, end_date, driver)
    print(start_date, end_date, dining_name)
    # blog_postings의 date, text, title 가져오기
    total_list = []

    for posting_addr in blog_posting_urls:
        date = get_element(DATE, posting_addr, driver,PAGE_COUNT)
        PAGE_COUNT = 1
        text = get_element(TEXT, posting_addr, driver,PAGE_COUNT)

        title = get_element(TITLE, posting_addr, driver,PAGE_COUNT)

        comment = get_element(COMMENT, posting_addr, driver,PAGE_COUNT)
        PAGE_COUNT = 0
        total_list.append([date,title,text,comment])


    save_tweet_data_to_csv(total_list, XLSX_PATH)
