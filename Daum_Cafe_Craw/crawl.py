from bs4 import BeautifulSoup
from urllib import request, parse
from selenium import webdriver
import time
import re
from settings import WEB_DRIVER_PATH
from settings import Craw_PAGE_COUNT
import xlwt
import csv
import requests

DATE = 0
TITLE = 1
TEXT = 2
COMMENT = 3

def make_basic_url(keyword, start, end):
    query = '&q='
    base_url = 'https://search.daum.net/search?w=cafe'
    DA = '&DA=STC'
    enc = '&enc=utf8'
    if isinstance(keyword,tuple):
        for key in keyword:
            query += parse.quote(key) + ","
    else:
        query += parse.quote(keyword)
    period = '&period=u' + '&sd=' + start + '000000' + '&ed=' + end + '235959'
    final_url = base_url + DA + enc + query + period
    return final_url

def get_blog_posting_urls(keyword, start, end, driver):
    basic_url = make_basic_url(keyword, start, end)
    blog_postings = []
    index = 1
    count = 0
    flag = True
    while(flag):
        if count == Craw_PAGE_COUNT: # 크롤 페이지 수
            flag = False
            break;
        else:
            count += 1
        # index에 해당하는 url
        url = basic_url + '&p=' + str(index)
        driver.implicitly_wait(1)
        driver.get(url)
        html = driver.page_source
        bs = BeautifulSoup(html, 'html5lib')
        for single_link in bs.find("div", class_="coll_cont").find_all("a", class_="f_link_b"):
            href = single_link['href']
            if href != None and href !=[]:
                if href in blog_postings:
                    break;
                else:
                    blog_postings.append(href)
        index += 1
    return blog_postings

def get_element(type, posting_addr, driver,PAGE_COUNT):
    url = posting_addr
    if PAGE_COUNT == 0:
        print(posting_addr)
        driver.get(url)
        driver.implicitly_wait(1)
        frame = driver.find_element_by_id("down")
        driver.switch_to.frame(frame)

    time.sleep(1)
    html = driver.page_source
    bs = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    switcher = {
        0: get_date,
        1: get_title,
        2: get_text,
        3: get_comment
    }
    return switcher.get(type)(bs,driver)

def get_date(bs,driver):
    for date_spans in bs.find_all("span", class_="txt_item")[2]:
        try:
            return date_spans.string
        except IndexError:
            return None

def get_text(bs,driver):
    # 네이버는 에디터에 따라 css selctor가 달라진다
    #user_contents
    text_divs = bs.find("div", class_="board_post tx-content-container")
    text_for_blog = ''
    for text in text_divs:
        text = re.sub(r'(\<.+?\>)', '', str(text))
        if text not in text_for_blog:
            text_for_blog += text.replace('&gt;','>').replace('&lt;','<').replace('&amp;','&').replace('&nbsp;','')
    return text_for_blog.strip().replace('document.write(removeRestrictTag());','')

def get_title(bs,driver):
    try:
        for title_divs in bs.find_all("div", class_="bbs_read_tit").find("strong", class_="tit_info"):
            for title in title_divs:
                final_title = re.sub(r'(\s\s[\s]+)', '', str(title.text))
                return final_title
    except:
        return None

def get_comment(bs,driver):
    result = []
    try:
        comment_divs=bs.find("div", class_="comment_view")
        comment_link=comment_divs.find_all("span", class_="original_comment")
        for comment in comment_link:
            if comment.text == '관리자의 승인을 기다리고 있는 댓글입니다':
                continue
            result.append(comment.text)
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