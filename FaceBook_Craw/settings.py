import os

WEB_DRIVER_PATH = 'C:\chromedriver.exe'
Facebook_id = '01045299351'
Facebook_pw = 'dltmdgud9351!@'
START_DATE = ['2021-03-24']
END_DATE =   ['2021-03-25']
DINING_NAME = ['아티장베이커리']
XLSX_PATH = os.path.dirname(os.path.abspath(__file__)) + str(START_DATE) + '_' + str(END_DATE) + '_' + str(DINING_NAME) + '.csv'