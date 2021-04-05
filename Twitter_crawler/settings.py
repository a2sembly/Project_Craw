import os

WEB_DRIVER_PATH = 'C:\chromedriver.exe'
Twitter_id = "lee_seunghyeong"
Twitter_pw = "dltmdgud9351!@"
START_DATE = ['2020-07-01']
END_DATE =   ['2020-07-02']
DINING_NAME = ['베이커리']
XLSX_PATH = os.path.dirname(os.path.abspath(__file__)) + str(START_DATE) + '_' + str(END_DATE) + '_' + str(DINING_NAME) + '.csv'

def alert(str):
    print("--------------------------------------------------------------------------------")
    print(str)
    print("--------------------------------------------------------------------------------")