from bs4 import BeautifulSoup
from urllib import request, parse
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import re
from settings import *
import xlwt
import pyperclip
import csv

DATE = 0
TITLE = 1
TEXT = 2
COMMENT = 3

def copy_input(xpath, input,driver):
    pyperclip.copy(input)
    driver.find_element_by_xpath(xpath).click()
    #클립보드 내용 붙여넣기
    ActionChains(driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()
    time.sleep(1)

def login_naver(id,pw,driver):
    alert('[+] Login Naver')
    driver.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
    time.sleep(1)

    copy_input('//*[@id="id"]', id,driver)
    time.sleep(1)
    copy_input('//*[@id="pw"]', pw,driver)
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="frmNIDLogin"]/fieldset/input').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="new.dontsave"]').click()
    
def make_basic_url(keyword, start, end):
    base_url = 'https://m.search.naver.com/search.naver?display=15&nso=p%3A'
    period = 'from' + start + 'to' + end
    query = '&query=' + parse.quote(keyword)
    end = '&where=m_article&start='
    final_url = base_url + period + query + end
    return final_url

def get_cafe_posting_urls(keyword, start, end, driver):
    basic_url = make_basic_url(keyword, start, end)
    cafe_postings = []
    index = 1
    count = 0
    flag = True
    while(flag):
        if count == 1:
            flag = False
            break;
        else:
            count += 1
        # index에 해당하는 url
        url = basic_url + str(index)
        driver.implicitly_wait(3)
        driver.get(url)
        driver.implicitly_wait(1)
        html = driver.page_source
        bs = BeautifulSoup(html, 'html5lib')
        for single_link in bs.find("ul", class_="lst_total _list_base").find_all("li", class_="bx _item"):
            for link in single_link.findAll('a', {'class': 'api_txt_lines total_tit'}):
                try:
                    href = link['href']
                    cafe_postings.append(href)
                except KeyError:
                    pass
        index += 15
    return cafe_postings

def get_element(type, posting_addr, driver,PAGE_COUNT):
    url = posting_addr
    if PAGE_COUNT == 0:
        print(url)
        driver.get(url)
        driver.implicitly_wait(5)
        
    time.sleep(1)   
    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    switcher = {
        0: get_date,
        1: get_title,
        2: get_text,
        3: get_comment
    }
    return switcher.get(type)(bs)

def get_date(bs):
    date_divs = bs.select('#ct > div:nth-child(1) > div > div.user_wrap > div:nth-child(3) > span.date.font_l')
    try:
        date = re.findall(r'(20[\d\s\.\:]*)', str(date_divs))[0]
        return date
    except:
        return None

def get_title(bs):
    try:
        title_divs = bs.select('#ct > div:nth-child(1) > div > h2')
        title = title_divs[0].text.replace('\n        ','')
        return title
    except:
        return None
 
def get_text(bs):
    try:
        post_divs = bs.select('#postContent')
        post = post_divs[0].text.split("투표")[0]
        return post
    except:
        return None

def get_comment(bs):
    result = []
    try:
        for comment_uls in bs.select('#ct > div.CommentComponent > div.section_comment > ul'):
            # ('a', {'class': 'api_txt_lines total_tit'}):
            for comment in comment_uls.findAll('p', {'class': 'txt'}):
                result.append(comment['v-if'])
        
        return result
    except:
        return None

def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['Date', 'Title', 'Post', 'Comment']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerows(records)