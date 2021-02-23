# -*- coding: UTF-8 -*-
import sys
import urllib2
import re
import xlwt
import time
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

def getValue(res, key):
    try:
        result = res[key]
    except:
        result = ''
    return result

link_list = []
base_url = 'http://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_s1398-s7074-s6500-s6502-s6106_1_1__'
for i in range(1, 581):    #1,581, 总页数 https://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_s1398-s7074-s6500-s6502-s6106_1_1__1.html#showc
    url = base_url + str(i) + '.html#showc'
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    ul = soup.find('ul', class_='result_list')
    print url
    temp = ul.find_all('a', text='更多参数>>')
    for link in temp:
        link_list.append('http://detail.zol.com.cn' + link['href'])

res_list = []
for url in link_list:
    print url
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page, 'html.parser')
    result = {}
    for linebreak in soup.find_all('br'):
        linebreak.extract()

    div = soup.find('div',class_='breadcrumb')
    a_list = div.find_all('a')
    brand = a_list[2].get_text()
    model = a_list[3].string
    result['brand'] = brand
    result['model'] = model
    tables = soup.findAll('table')
    for table in tables:
        tr_arr = table.find_all("tr")
        for tr in tr_arr:
            if tr.find('td',text='外观') or tr.find('td',text='手机附件') or tr.find('td',text='保修信息'):
                break
            else:
                if tr.find('th') is not None:
                    key = tr.find('th').get_text().strip()
                    spans = tr.find_all('span')
                    value = spans[-1].string
                    if value == None:
                        value = ''
                        temp = spans[-1].stripped_strings
                        for i in temp:
                            value += i + ','
                    result[key] = value

    try:
        system = result[u'操作系统']
        if 'Android' in system:
            pattern = re.compile("Android.{0,}", re.S)
            items = re.findall(pattern, system)
            try:
                android = str(items[0])
            except:
                android = ''
        else: android = ''
    except:
        android = ''
    result['android'] = android

    try:
        span  = soup.find('span',text='连接与共享')
        temp = span.parent.find_all('span')[1]
        hasOTG =  'OTG' in temp.strings
        if hasOTG:
            result['OTG'] = 'Y'
        else:
            result['OTG'] = 'N'
    except:
        result['OTG'] = 'N'
    for key in result:
        pass
        print "key is [" +key +"], result is ["+ str(result[key]) +"]"
    res_list.append(result)

workbook = xlwt.Workbook(encoding='utf8')                          #创建工作簿
sheet1 = workbook.add_sheet(u'手机参数表', cell_overwrite_ok=True)  # 创建sheet
row0 = [u'品牌', u'机型', u'上市日期', u'电商报价',u'OS版本', u'操作系统', u'内存',
        u'扩展容量', u'CPU型号', u'CPU核心数', u'CPU频率', u'GPU型号', u'存储卡', u'摄像头', u'电池容量', '视频支持',u'音频支持']
for i in range(0, len(row0)):
    sheet1.write(0, i, row0[i])
row_index = 1
for res in res_list:
        rows = [
            getValue(res, 'brand'),
            getValue(res, 'model'),
            getValue(res, u'上市日期'),
            getValue(res, u'电商报价'),
            getValue(res, u'出厂系统内核'),
            getValue(res, u'操作系统'),
            getValue(res, u'存储类型'),
            getValue(res, u'扩展容量'),
            getValue(res, u'CPU型号'),
            getValue(res, u'核心数'),
            getValue(res, u'CPU频率'),
            getValue(res, u'GPU型号'),
            getValue(res, u'存储卡'),
            getValue(res, u'视频拍摄'),
            getValue(res, u'电池容量'),
            getValue(res, u'视频支持'),
            getValue(res, u'音频支持')
        ]
        for i in range(len(rows)):
            sheet1.write(row_index, i, rows[i])
        row_index += 1
t = str(time.time())
workbook.save(t + '.xls')  # 保存文件


