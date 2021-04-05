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
    print('make_basic_url')
    base_url = 'https://search.daum.net/search?w=blog'
    DA = '&DA=STC'
    enc = '&enc=utf8'
    query = '&q=' + parse.quote(keyword)
    f = '&f=section'
    SA = '&SA=daumsec'
    period = '&sd=' + start + '000000' + '&ed=' + end + '235959' + '&period=u'
    final_url = base_url + DA + enc + query + f + SA + period
    return final_url

def get_blog_posting_urls(keyword, start, end, driver):
    print('get_blog_posting_urls')
    basic_url = make_basic_url(keyword, start, end)
    blog_postings = []
    index = 1
    count = 0
    flag = True
    regex_href = r'.*http:\/\/blog\.daum\.net\/(\w*\/\d*)'
    while(flag):
        if count == Craw_PAGE_COUNT: # 크롤 페이지 수
            flag = False
            break;
        else:
            print(count)
            count += 1
        # index에 해당하는 url
        url = basic_url + '&page=' + str(index)
        driver.implicitly_wait(1)
        driver.get(url)
        html = driver.page_source
        bs = BeautifulSoup(html, 'html5lib')
        for single_link in bs.find("div", class_="coll_cont").find_all("a", class_="f_link_b"):
            # single_link가 https://m.blg.naver.com을 포함하면 그걸 가져오자
            href = re.findall(regex_href, str(single_link))
            if href != None and href !=[]:
                if href in blog_postings:
                    break;
                else:
                    blog_postings.append(href)
                    print(href)
        index += 1
    return blog_postings

def get_element(type, posting_addr, driver,PAGE_COUNT):
    url = 'https://m.blog.daum.net/' + posting_addr[0]
    if PAGE_COUNT == 0:
        print('https://m.blog.daum.net/' + posting_addr[0])
        driver.get(url)

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
    date_divs = bs.select('#mArticle > div > div.blogview_info > time')
    date = re.findall(r'(20[\d\s\.\:]*)', str(date_divs))
    try:
        return date[0]
    except IndexError:
        return None

def get_text(bs,driver):
    # 네이버는 에디터에 따라 css selctor가 달라진다
    text_divs = bs.select('#mArticle > div > div.blogview_content.useless_p_margin')

    text_for_blog = ''
    for text in text_divs:
        text = re.sub(r'(\<.+?\>)', '', str(text))
        if text not in text_for_blog:
            text_for_blog += text.replace('&gt;','>').replace('&lt;','<').replace('&amp;','&').replace('&nbsp;','')
    return text_for_blog.strip()

def get_title(bs,driver):
    title_divs = bs.select('#kakaoWrap > div.blogview_head > h2')
    if title_divs == []:
        title_divs = bs.select('#mArticle > div > div.blogview_tit > h2')
    for title in title_divs:
        final_title = re.sub(r'(\s\s[\s]+)', '', str(title.text))
        return final_title

def get_comment(bs,driver):
    result = []
    comment_divs = None
    comment_link = None
    try:
        while(1):
            comment_more=bs.find("a", class_="link_cmtmore")
            if comment_more != None:
                driver.find_element_by_xpath('//*[@id="comment"]/div/div/a').click()
            else:
                break

        comment_divs=bs.find("ul", class_="list_cmt")
        comment_link=comment_divs.find_all("span", class_="txt_cmt")
        for comment in comment_link:
            if comment.text in '관리자의 승인을':
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