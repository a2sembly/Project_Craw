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
    base_url = 'https://m.search.naver.com/search.naver?display=15&nso=p%3A'
    period = 'from' + start + 'to' + end
    query = '&query=' + parse.quote(keyword)
    end = '&where=m_blog&start='
    final_url = base_url + period + query + end
    return final_url

def get_blog_posting_urls(keyword, start, end, driver):
    basic_url = make_basic_url(keyword, start, end)
    blog_postings = []
    index = 1
    count = 0
    flag = True
    regex_href = r'.*https:\/\/m\.blog\.naver\.com\/(\w*\/\d*)'
    while(flag):
        if count == Craw_PAGE_COUNT: # 크롤 페이지 수
            flag = False
            break;
        else:
            count += 1
        # index에 해당하는 url
        url = basic_url + str(index)
        driver.implicitly_wait(1)
        driver.get(url)
        html = driver.page_source
        bs = BeautifulSoup(html, 'html5lib')
        for single_link in bs.find("ul", class_="lst_total _list_base").find_all("li", class_="bx _item"):
        # single_link가 https://m.blg.naver.com을 포함하면 그걸 가져오자
            href = re.findall(regex_href, str(single_link))
            if href != None and href !=[]:
                if href in blog_postings:
                    break;
                else:
                    blog_postings.append(href)
        index += 15
    return blog_postings

def get_element(type, posting_addr, driver,PAGE_COUNT):
    url = 'https://m.blog.naver.com/' + posting_addr[0]
    if PAGE_COUNT == 0:
        print('https://m.blog.naver.com/' + posting_addr[0])
        driver.get(url)
    time.sleep(1)
    html = driver.page_source.encode('utf-8')
    bs = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')

    switcher = {
        0: get_date,
        1: get_title,
        2: get_text,
        3: get_comment
    }
    return switcher.get(type)(bs,driver)

def get_date(bs,driver):
    date_divs = bs.select('.se_date')
    date = re.findall(r'(20[\d\s\.\:]*)', str(date_divs))
    try:
        return date[0]
    except IndexError:
        return None

def get_text(bs,driver):
    # 네이버는 에디터에 따라 css selctor가 달라진다
    text_divs1 = bs.select('.se_textView > .se_textarea > span,p')
    text_divs2 = bs.select('.post_ct span')

    if len(text_divs1) > len(text_divs2):
        final_text_div = text_divs1
    else:
        final_text_div = text_divs2

    text_for_blog = ''
    for text in final_text_div:
        text = re.sub(r'(\<.+?\>)', '', str(text))
        if text not in text_for_blog:
            text_for_blog +=text.replace('&gt;','>').replace('&lt;','<').replace('&amp;','&').replace('&nbsp;','')
    return text_for_blog.strip().replace('본문 기타 기능본문 폰트 크기 작게 보기본문 폰트 크기 크게 보기가','').replace('로그인이 필요합니다.ⓒ NAVER Corp.','')

def get_title(bs,driver):
    title_divs = bs.select('.se_title > .se_textView > .se_textarea')
    if title_divs == []:
        title_divs = bs.select('.tit_h3')
    for title in title_divs:
        final_title = re.sub(r'(\s\s[\s]+)', '', str(title.text))
        return final_title

def get_comment(bs,driver):
    result = []
    try:
        comment_divs=bs.find("div", class_="section_w")
        comment_link=comment_divs.find("a", class_="btn_reply")
        url = 'https://m.blog.naver.com/' + comment_link['href']
        # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Whale/2.9.115.16 Safari/537.36'
        # headers = {'User-Agent': user_agent}
        # rep = requests.get(url,headers=headers)
        # print(rep.text)
        driver.get(url)
        html = driver.page_source
        bs_c = BeautifulSoup(html, 'html5lib', from_encoding='utf-8')
        for comment in bs_c.findAll('span', {'class': 'u_cbox_contents'}):
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