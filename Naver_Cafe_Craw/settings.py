import os

WEB_DRIVER_PATH = 'C:\chromedriver.exe'
naver_id = ''
naver_pw = ''
START_DATE = ['20170507']
END_DATE =   ['20180706']
DINING_NAME = [('친환경','소비')]
XLSX_PATH = os.path.dirname(os.path.abspath(__file__)) + str(START_DATE) + '_' + str(END_DATE) + '_' + str(DINING_NAME) + '.csv'

def alert(str):
    print("--------------------------------------------------------------------------------")
    print(str)
    print("--------------------------------------------------------------------------------")