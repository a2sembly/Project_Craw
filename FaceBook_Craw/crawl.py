from bs4 import BeautifulSoup
from urllib import request, parse
from selenium import webdriver
import time
import re
from settings import WEB_DRIVER_PATH
import xlwt
import csv
import requests
import base64
from settings import Facebook_id
from settings import Facebook_pw
from selenium.webdriver.common.alert import Alert

DATE = 0
TEXT = 2

def make_basic_url(keyword, start, end):
    '''{"rp_creation_time:0":"{\"name\":\"creation_time\",\"args\":\"{\\\"start_day\\\":\\\"2020-1-1\\\",\\\"end_day\\\":\\\"2020-1-2\\\"}\"}"}'''
    print('make_basic_url')
    base_url = 'https://www.facebook.com/search/posts?'
    query = 'q=' + parse.quote(keyword)
    filter_= '{"rp_creation_time:0":"{\\"name\\":\\"creation_time\\",\\"args\\":\\"{\\\\\\\"start_day\\\\\\\":\\\\\\\"' + start + '\\\\\\\",\\\\\\\"end_day\\\\\\\":\\\\\\\"' + end + '\\\\\\\"}\\"}"}'
    filters = '&filters=' +  str(base64.b64encode(filter_.encode('ascii')).decode())
    final_url = base_url + query + filters
    return final_url

def scroll_down_page(driver, last_position, num_seconds_to_load=0.5, scroll_attempt=0, max_attempts=5):
    end_of_scroll_region = False
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(num_seconds_to_load)
    curr_position = driver.execute_script("return window.pageYOffset;")
    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            end_of_scroll_region = True
        else:
            scroll_down_page(last_position, curr_position, scroll_attempt + 1)
    last_position = curr_position
    return last_position, end_of_scroll_region

def Facebook_login(driver):
    driver.get("http://www.facebook.com")
    # Step 3) Search & Enter the Email or Phone field & Enter Password
    username = driver.find_element_by_id("email")
    password = driver.find_element_by_id("pass")
    submit   = driver.find_element_by_name("login")
    username.send_keys(Facebook_id)
    password.send_keys(Facebook_pw)
    # Step 4) Click Login
    submit.click()

def Facebook_postings_urls(keyword, start, end, driver,title_list,date_list):
    last_position = None
    end_of_scroll_region = False
    basic_url = make_basic_url(keyword, start, end)
    blog_postings = []
    flag = True
    driver.implicitly_wait(1)
    Facebook_login(driver)
    time.sleep(1)
    driver.get(basic_url)
    time.sleep(2)
    while not end_of_scroll_region:
        last_position, end_of_scroll_region = scroll_down_page(driver, last_position)

    time.sleep(2)
    html = driver.page_source
    time.sleep(0.5)
    bs = BeautifulSoup(html, 'html5lib')
    for single_link in bs.findAll('div', {'role': 'article'}):
        href = single_link.findAll('a', {'role': 'link'})[1]['href']
        title = single_link.findAll('a', {'role': 'link'})[0].string
        if title != None and title !=[]:
            title_list.append(title)
            print(title)

        if href != None and href !=[]:
            if href in blog_postings:
                continue;
            else:
                blog_postings.append(href)
                print(href)
    return blog_postings
# #jsc_c_5f > span:nth-child(2) > span > a > span > span > b > b:nth-child(4)
# #mount_0_0_JY > div > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div:nth-child(1) > div > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.pfnyh3mw.d2edcug0.hpfvmrgz.hybvsw6c.gitj76qy.dp1hu0rb.kelwmyms.dzul8kyi.e69mrdg2 > div > div > div > div.j83agx80.cbu4d94t.buofh1pr.l9j0dhe7 > div.dati1w0a.f10w8fjw.hv4rvrfc.discj3wi > div:nth-child(1) > div.btwxx1t3.j83agx80.hybvsw6c.ll8tlv6m > div.buofh1pr > div > div:nth-child(2) > span > span > span:nth-child(2) > span > a > span > span > b > b:nth-child(22)
def get_element(type, posting_addr, driver,PAGE_COUNT):
    if PAGE_COUNT == 0:
        driver.get(posting_addr.replace('www','m'))

    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    switcher = {
        0: get_date,
        2: get_text,
    }
    return switcher.get(type)(bs,driver)

def get_date(bs,driver):
    #//*[@id="MPhotoUpperContent"]/div/div/div[1]/div/div/div[1]/div
    #//*[@id="u_0_u_3y"]/div[1]/div[1]/div
    #data-sigil="m-feed-voice-subtitle"
    #div.story_body_container > div._5rgt._5nk5
    date_divs = bs.findAll('div', {'data-sigil': 'm-feed-voice-subtitle'})
    date_divs_1 = bs.findAll('abbr', {'data-sigil': 'timestamp'})
    try:
        if len(date_divs) > len(date_divs_1):
            final_text = date_divs
        else:
            final_text = date_divs_1

        date = final_text[0].get_text().replace('·','')
        return date
    except IndexError:
        return None

def get_text(bs,driver):
    try:
        # 네이버는 에디터에 따라 css selctor가 달라진다
        text_divs = bs.findAll('div', {'data-ft': '{\"tn\":\"*s\"}'})
        text_divs_other = bs.findAll('a', {'class': 'actor-link'})

        if len(text_divs) > len(text_divs_other):
            final_text = text_divs
        else:
            final_text = text_divs_other.findAll('div', {'class': ''})

        text_for_facebook = ''
        for text in final_text:
            text = re.sub(r'(\<.+?\>)', '', str(text))
            if text not in text_for_facebook:
                text_for_facebook += text
        return text_for_facebook.replace('&nbsp;','')
    except:
        return None

def save_tweet_data_to_csv(records, filepath, mode='a+'):
    header = ['Date', 'Title', 'Post']
    with open(filepath, mode=mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if mode == 'w':
            writer.writerow(header)
        if records:
            writer.writerows(records)