import os

WEB_DRIVER_PATH = 'C:\chromedriver.exe'
START_DATE = ['20170507']
END_DATE =   ['20180706']
DINING_NAME = ['아티장베이커스']
XLSX_PATH = os.path.dirname(os.path.abspath(__file__)) + str(START_DATE) + '_' + str(END_DATE) + '_' + str(DINING_NAME) + '.csv'
Craw_PAGE_COUNT = 5