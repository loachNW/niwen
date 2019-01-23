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


def url_open(url):
    res = request.Request(url)
    res.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
    try:
        html = request.urlopen(res,timeout = 60).read()
    except:
        html = request.urlopen(res, timeout=60).read()
    return html

def post(page,type):
    url = 'http://www.sczwfw.gov.cn/app/powerDutyList/getThImplement' # 网址
    data = {}
    data['fields'] = ''
    data['pageSize'] = '10'
    data['page'] = page
    data['eventType'] = type
    data['deptCode'] = ''
    data['eventName'] = ''
    data['onlineType'] = ''
    data['areaCode'] = '510100000000'
    data = urllib.parse.urlencode(data).encode('utf-8')  # 转化data格式为
    res = request.urlopen(url,data)
    html = res.read().decode('utf-8')
    return html


def theme(data):
    html = lxml.html.fromstring(data)  # 等同于etree.HTML函数
    data_theme = ""
    a = html.cssselect('#tab_sdyj > tfoot > tr')
    for i in range(len(a)):
        if (len(html.cssselect('#tab_sdyj > tfoot > tr:nth-child('+ str(i+1)+') > td:nth-child(2)'))!= 0) and (len(html.cssselect('#tab_sdyj > tfoot > tr:nth-child('+ str(i+1)+') > td:nth-child(6)'))!= 0):
            data_theme += html.cssselect('#tab_sdyj > tfoot > tr:nth-child('+ str(i+1)+')')[0].text_content()
    return(data_theme)


def getdata(url):
    htmlstr = url_open(url).decode("utf-8")#打开网页并解码，得到网页源码
    return(htmlstr)

def get_id1(html):
    a = re.findall('"thDirectoryId":"(\d+)"',html)
    return a

def geturllist():
    pass

def get_id(html):
    id = re.findall('id=(\d+)%',html)
    return(id)


def get_id2(html):
    a = re.findall('"idForStr":"(\d+)",', html)
    return a

def main():
    rightNo = 0
    os.chdir('C:/Users/ASUS/Desktop/')
    righttype = ["行政许可", "行政处罚", "行政强制", "行政征收", "行政裁决", "行政确认", "行政给付", "行政奖励", "行政检查", "其他行政权力"]
    righttype_code = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I", "1Z"]
    page_max = [27, 452, 14, 3, 1, 2, 1, 8, 19, 5]  # 每一个的页码
    with open('四川.json','w', encoding = 'utf-8') as json_file:
        json_file.write('[\n')
        for type in range(0,10):
            print(righttype[type])
            for i in range(page_max[type]):
                print(i)
                html = post(str(i + 1),righttype_code[type])
                id_1 = get_id1(html)
                id_2 = get_id2(html)
                if len(id_2) > 0:
                    eventname = re.findall('"eventName":"(.+?)"', html)  # 用了个正则
                    performDeptName = re.findall('"performDeptName":"(.+?)"', html)  # 包括上一行提取两个信息
                    for j in range(len(eventname)):
                        if(id_2[j] !='0'):
                            map = {}
                            map['rightname'] = eventname[j]
                            map['righttype'] = righttype[type]
                            map['executorName'] = performDeptName[j]
                            map['url'] = 'http://cds.sczwfw.gov.cn/app/main?areaCode=510100000000&iframeUrlLo=workGuide/detail?id=' + id_2[j] +'%26shardKey=5101%26typeflag=3'
                            json.dump(map, json_file)
                            json_file.write(",\n")
                            rightNo += 1
                print("已爬取" + str(rightNo))
                for k in id_1:
                    url = 'http://cds.sczwfw.gov.cn/app/thing/findByThDirectory?eventName=&areaCode=510100000000&eventType=1&deptCode=&onlineType=&thDirectoryId=' + k
                    html = url_open(url).decode()
                    id_2 = get_id2(html)
                    eventname = re.findall('"eventName":"(.+?)"', html)  # 用了个正则
                    performDeptName = re.findall('"performDeptName":"(.+?)"', html)  # 包括上一行提取两个信息
                    for z in range(len(eventname)):
                        map = {}
                        map['rightname'] = eventname[z]
                        map['righttype'] = righttype[type]
                        map['executorName'] = performDeptName[z]
                        map[ 'url'] = 'http://cds.sczwfw.gov.cn/app/main?areaCode=510100000000&iframeUrlLo=workGuide/detail?id=' + id_2[z] + '%26shardKey=5101%26typeflag=3'
                        json.dump(map, json_file)
                        json_file.write(",\n")
                        rightNo += 1
        json_file.write('' '\n]')
main()

os.chdir('C:/Users/ASUS/Desktop/')
with open("detil_id.json", encoding="utf-8") as json_file:
    table = json.load(json_file)
json_file.close
table[0]["key"] = "value"
def rightlist():
    rightNo = 0
    os.chdir('C:/Users/ASUS/Desktop/')
    with open('四川权力清单.json', 'w', encoding="utf-8") as f:
        f.write('[\n')
        for i in range(len(table)):
            id = get_id(table[i]["sourceUrl"])#每一条id
            Url = 'http://www.sczwfw.gov.cn/app/workGuide/detail?id=' + id[0] + '&shardKey=5101&typeflag=3'
            try:
                data = getdata(Url)
            except:
                print('此处出错：', table[i] ,Url)
            data_theme = theme(data)
            if  data_theme != "":
                json.dump(data_theme,f)
                f.write(',\n\n\n')
                rightNo +=1
                print(rightNo)
            else:
                data_theme = '无法律依据'
                json.dump(data_theme, f)
                f.write(',\n\n\n')
                print('此网页没有内容：',Url)
                rightNo += 1
                print(rightNo)
        f.write('' '\n]')
rightlist()


#补充，自写代码
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



def getdata(url):
    htmlstr = url_open(url).decode("utf-8")#打开网页并解码，得到网页源码
    return(htmlstr)




def url_open(url):
    res = request.Request(url)
    res.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
    try:
        html = request.urlopen(res,timeout = 60).read()
    except:
        html = request.urlopen(res, timeout=60).read()
    return html


def get_id(html):
    id = re.findall('id=(\d+)%',html)
    return(id)

def theme(data):
    html = lxml.html.fromstring(data)  # 等同于etree.HTML函数
    data_theme = ""
    a = html.cssselect('#tab_sdyj > tfoot > tr')
    for i in range(len(a)):
        if (len(html.cssselect('#tab_sdyj > tfoot > tr:nth-child('+ str(i+1)+') > td:nth-child(2)'))!= 0) and (len(html.cssselect('#tab_sdyj > tfoot > tr:nth-child('+ str(i+1)+') > td:nth-child(6)'))!= 0):
            data_theme += html.cssselect('#tab_sdyj > tfoot > tr:nth-child('+ str(i+1)+')')[0].text_content()
    return(data_theme)



os.chdir('C:/Users/ASUS/Desktop/')
with open("detil_id.json", encoding="utf-8") as json_file:
    table = json.load(json_file)
json_file.close
table = table[0:40]
table[0]["key"] = "value"
def rightlist():
    rightNo = 0
    os.chdir('C:/Users/ASUS/Desktop/')
    with open('四川权力清单.json', 'w', encoding="utf-8") as f:
        f.write('[\n')
        for i in range(len(table[0:40])):
            id = get_id(table[i]["sourceUrl"])#每一条id
            Url = 'http://www.sczwfw.gov.cn/app/workGuide/detail?id=' + id[0] + '&shardKey=5101&typeflag=3'
            try:
                data = getdata(Url)
            except:
                print('此处出错：', table[i] ,Url)
            data_theme = theme(data)
            if  data_theme != "":
                json.dump(data_theme,f)
                f.write(',\n\n\n')
                rightNo +=1
                print(rightNo)
            else:
                data_theme = '无法律依据'
                json.dump(data_theme, f)
                f.write(',\n\n\n')
                print('此网页没有内容：',Url)
                rightNo += 1
                print(rightNo)
        f.write(' \n]')
rightlist()




