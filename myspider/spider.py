import requests
import bs4
import os
import datetime
import time

def fetchUrl(url):  #访问网页，获取网页内容并返回
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    return r.text

def getPageList(year, month, day):  #获取x年x月x日各版面的链接列表
    url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/nbs.D110000renmrb_01.htm'    #url格式固定
    html = fetchUrl(url)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    temp = bsobj.find('div', attrs = {'id': 'pageList'})
    if temp:
        pageList = temp.ul.find_all('div', attrs = {'class': 'right_title-name'})
    else:
        pageList = bsobj.find('div', attrs = {'class': 'swiper-container'}).find_all('div', attrs = {'class': 'swiper-slide'})
    linkList = []

    for page in pageList:
        link = page.a["href"]
        url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
        linkList.append(url)

    return linkList

def getTitleList(year, month, day, pageUrl):    #获取版面内的文章链接列表
    html = fetchUrl(pageUrl)
    bsobj = bs4.BeautifulSoup(html, 'html.parser')
    temp = bsobj.find('div', attrs = {'id': 'titleList'})
    if temp:
        titleList = temp.ul.find_all('li')
    else:
        titleList = bsobj.find('ul', attrs = {'class': 'news-list'}).find_all('li')

    linkList = []

    for title in titleList:
        tempList = title.find_all('a')
        for temp in tempList:
            link = temp["href"]
            if 'nw.D110000renmrb' in link:
                url = 'http://paper.people.com.cn/rmrb/html/' + year + '-' + month + '/' + day + '/' + link
                linkList.append(url)

    return linkList

def getContent(html,url):   # 解析网页，获取网页内容
    bsobj = bs4.BeautifulSoup(html, 'html.parser')

    urlout='连接：'+url+'\n'
    # 获取文章 标题
    title = '标题：'+bsobj.h3.text + '\n' + bsobj.h1.text + '\n' + bsobj.h2.text + '\n'
    # print(title)
    # 获取文章 内容
    pList = bsobj.find('div', attrs={'id': 'ozoom'}).find_all('p')
    content = '内容：\n'
    for p in pList:
        content += p.text + '\n'
        # print(content)
    res = urlout + title + content
    return res

def saveFile(content, path, filename):  #文章内容保存到本地文件
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)

def download_rmrb(year, month, day, destdir):   #爬x年x月x日的新闻内容，保存在指定目录下
    pageList = getPageList(year, month, day)
    for page in pageList:
        titleList = getTitleList(year, month, day, page)
        for url in titleList:
            html = fetchUrl(url)
            content = getContent(html,url)

            # 文件路径及文件名
            temp = url.split('_')[2].split('.')[0].split('-')
            pageNo = temp[1]
            titleNo = temp[0] if int(temp[0]) >= 10 else '0' + temp[0]
            path = destdir + '/' + year + month + day + '/'
            fileName = year + month + day + '-' + pageNo + '-' + titleNo + '.txt'

            saveFile(content, path, fileName)


def gen_dates(date, days):
    day = datetime.timedelta(days=1)
    for i in range(days):
        yield date + day * i


def get_date_list(beginDate, endDate):  #获取日期列表
    start = datetime.datetime.strptime(beginDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")
    data = []
    for d in gen_dates(start, (end - start).days):
        data.append(d)

    return data


if __name__ == '__main__':

    beginDate = input('开始日期（格式yyyymmdd）:')
    endDate = input('结束日期（格式yyyymmdd）:')
    data = get_date_list(beginDate, endDate)
    datapath='../data'      #爬取数据存放位置

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >= 10 else '0' + str(d.month)
        day = str(d.day) if d.day >= 10 else '0' + str(d.day)
        download_rmrb(year, month, day, datapath)
        print("爬取完成：" + year + month + day)
        time.sleep(3)
