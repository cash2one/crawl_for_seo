#!/usr/bin/env python
#coding: utf-8

import requests
import re
import json
from BeautifulSoup import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

keywords = ['天使汇', 'tech2ipo', '羊羊羊']

PAGE_COUNT = 2

PC_URL = 'http://www.baidu.com/s?wd=%s&pn=%s0'
MOBILE_URL = 'http://m.baidu.com/s?word=%s'
ZHIDAO_URL = 'http://zhidao.baidu.com/search?word=%s'

def run():
    
    print '开始爬取PC端'
    with open('PC.csv', 'w+') as f:
        for k in keywords:
            print '爬取关键字：%s' % k
            f.write(run_pc(k))
            print '爬取内容写入文件完成\n\n'

    # run_mobile(keyword)
    # run_zhidao(keyword)


def run_pc(keyword):
    s = list()

    for page in range(PAGE_COUNT):
        print '开始获取第%s页内容' % str(page + 1)
        r = requests.get(PC_URL % (keyword, page))
        text = r.text
        save_to_file = 'pc_%s_page_%s.html' % (keyword, page + 1)
        print '网页保存至：%s' % save_to_file
        write(text, save_to_file)

        for i, o in enumerate(parse_pc(text)):
            rank = i 
            url = o[2]
            title = deal_title(o[3])
            
            if '%s的最新相关信息' % keyword in title:
                for o_ in get_news(text):
                    rank = i
                    url = o_[1]
                    title = deal_title(o_[2])
                    tmp = '%s,%s,%s,%s,%s\n' % (keyword, page + 1, i + 1, title, url)
                    #print_utf8(tmp)
                    s.append(tmp)

            else:
                tmp = '%s,%s,%s,%s,%s\n' % (keyword, page + 1, i + 1, title, url)
                #print_utf8(tmp)
                s.append(tmp)

           
    return ''.join(s)
        

def parse_pc(txt):
    p = '<h3 class="(t|t c-gap-bottom-small)">.*?<a.*?(data-click|).*?href\s?=\s?"(.*?)".*?>(.*?)<\/a>.*?<\/h3>'
    return re.findall(p, txt, re.S)


def get_news(txt):
    p = '(<div class="c-offset">(.*?)<div class="result)'
    m = re.findall(p, txt, re.S)
    m_ = None
    if m:
        txt = m[0][0]
        p = '<div class="(c-gap-bottom-small|c-row)">.*?<a href="(.*?)".*?>(.*?)</a>.*?</div>'
        m_ = re.findall(p, txt, re.S)

    return m_


def print_utf8(s):
    print json.dumps(s, encoding="UTF-8",  ensure_ascii=False)


def write(s, filename):
    with open(filename, 'w+') as f:
        f.write(s)


def deal_title(title):
    '''
    处理标题
    替换html字符
    处理空格
    处理逗号
    '''
    if title:
        title = title.strip()

        filter_list = ['<em>', '</em>', ',']
        for s in filter_list:
            title = title.replace(s, '')

    return title
    

if __name__ == '__main__':
    run()