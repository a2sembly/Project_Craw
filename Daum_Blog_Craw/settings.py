import os

WEB_DRIVER_PATH = 'C:\chromedriver.exe'
START_DATE = ['20030306']
END_DATE =   ['20210325']
DINING_NAME = ['철원 1경 고석정']
XLSX_PATH = os.path.dirname(os.path.abspath(__file__)) + str(START_DATE) + '_' + str(END_DATE) + '_' + str(DINING_NAME) + '.csv'
Craw_PAGE_COUNT = 5

def alert(str):
    print("--------------------------------------------------------------------------------")
    print(str)
    print("--------------------------------------------------------------------------------")