from urllib import request
import os
import time
import lxml
import lxml.html
from bs4 import BeautifulSoup
import re
import json
from urllib.parse  import urljoin
import requests
from lxml import etree
import cssselect
import numpy as np
from urllib import request
import os
import time
import lxml
import lxml.html
import re
import json
import urllib.parse
from lxml import etree
import requests
import cssselect
import json,xlwt




def url_open(url):
    count = 0
    res = request.Request(url)  #发送请求
    res.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134") #打开网页并读取内容  使用浏览器访问
    while count < 5:
        try:
            html = request.urlopen(res,timeout = 60).read()#打开网页并读取
            break
        except:
            count+=1
    return html #html里面为网页内容


def getcode(html):
    code = re.findall(r'href="(.+?question/\d+?.html)"', html)
    return code


def getquestion(html):
    html = etree.HTML(html)
    question = html.xpath('//*[@id="wgt-ask"]/h1/span[1]')
    return(question)

def getanswer(html):
    soup = BeautifulSoup(html, "html5lib")
    # html = lxml.html.fromstring(html)
    # data = html.cssselect('div.mb-10')
    # answer = data.text_content()[0]
    answer = soup.select("div.mb-10")[0].text
    return(answer)

def main():
    rightNo = 0
    os.chdir('C:/Users/ASUS/Desktop/')# 设置系统路径
    with open("公益诉讼.json","w",encoding = "utf-8") as json_file: #打开文件"海口1.json"
        json_file.write("[\n")  #以"[\n" 的格式存储
        page = np.linspace(0, 750, 750/ 10 + 1, dtype="int").tolist()
        for i in range(len(page)):
            url = 'https://zhidao.baidu.com/search?word=%B9%AB%D2%E6%CB%DF%CB%CF&ie=gbk&site=-1&sites=0&date=0&pn=' + str(page[i])
            html = url_open(url).decode("gbk")
            code = getcode(html)
            for j in range(len(code)):
                html2 = url_open(code[j]).decode("gbk")
                question = getquestion(html2)[0].text
                answer = getanswer(html2)
                if len(answer)<600:
                    rightNo += 1
                    print(rightNo, '第', i ,'页', j ,)
                    json.dump(question, json_file)  # 讲data放置到json文件中
                    json_file.write(',\n')
                    answer = re.sub('[展开全部]', '', answer)
                    json.dump(answer, json_file)  # 讲data放置到json文件中
                    json_file.write(',\n')
        json_file.write("' '\n]")
main()



def writeM():
    os.chdir('C:/Users/ASUS/Desktop/')
    with open("公益诉讼1.json", encoding='utf-8') as f:
        table = json.load(f)  # 将字符串转换为字典
    f.close()
    title = ["问题","答案",]
    book = xlwt.Workbook() # 创建一个excel对象
    sheet = book.add_sheet('Sheet1',cell_overwrite_ok=True) # 添加一个sheet页
    for i in range(len(title)): # 循环列
        sheet.write(0,i,title[i]) # 将title数组中的字段写入到0行i列中
    for j in range(len(table)):
        if j % 2 == 0:
            sheet.write(int(j/2),0, table[j])  # 将j写入到第int(j)行，第0列中
        else:
            sheet.write(int(j/2), 1, table[j])
        print(j)
    book.save('問答.xls')



if __name__ == '__main__':
    writeM()

