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
        html = request.urlopen(res,timeout = 60).read()
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



def get_id1(html):
    a = re.findall('"thDirectoryId":"(\d+)"',html)
    return a

def get_id2(html):
    a = re.findall('"idForStr":"(\d+)",', html)
    return a

def main():
    counts = 0
    rightType = ["行政许可", "行政处罚", "行政强制", "行政征收", "行政裁决", "行政确认", "行政给付", "行政奖励", "行政检查", "其他行政权力"]
    rightType_code = ["1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H", "1I", "1Z"]
    page_max = [27,452,14,3,1,2,1,8,19,5]
    os.chdir('C:/Users/ASUS/Desktop/')
    with open("detil_id.json", "w", encoding="utf-8") as json_file:
        json_file.write("[\n")
        for type in range(0,10):
            print(rightType[type])
            for i in range(page_max[type]):
                print(i)
                html = post(str(i+1),rightType_code[type])
                id_1 = get_id1(html)
                id_2 = get_id2(html) #两段代码都得到
                if len(id_2) > 0:#存在idForStr
                    eventname = re.findall('"eventName":"(.+?)"', html) #用了个正则
                    performDeptName = re.findall('"performDeptName":"(.+?)"', html)#包括上一行提取两个信息
                    for num in range(len(eventname)):
                        if(id_2[num]!="0"):
                            map = {}
                            map["rightName"] = eventname[num]
                            map["rightType"] = rightType[type]
                            map["executorName"] = performDeptName[num]
                            map["sourceUrl"] = "http://www.sczwfw.gov.cn/app/main?areaCode=510100000000&iframeUrlLo=workGuide/detail?id=" + id_2[num] + "%26shardKey=5101%26typeflag=3"
                            json.dump(map, json_file)
                            json_file.write(",\n")
                            counts +=1
                    print("已爬取"+str(counts))
                for j in id_1:
                    url = "http://www.sczwfw.gov.cn/app/thing/findByThDirectory?eventName=&areaCode=510100000000&eventType=1&deptCode=&onlineType=&thDirectoryId=" + j
                    html = url_open(url).decode()
                    id_2 = get_id2(html)
                    eventname = re.findall('"eventName":"(.+?)"',html)
                    performDeptName = re.findall('"performDeptName":"(.+?)"',html)
                    for num in range(len(eventname)):
                        map = {}
                        map["rightName"] = eventname[num]
                        map["rightType"] = rightType[type]
                        map["executorName"] = performDeptName[num]
                        map["sourceUrl"] = "http://www.sczwfw.gov.cn/app/main?areaCode=510100000000&iframeUrlLo=workGuide/detail?id=" + id_2[num] + "%26shardKey=5101%26typeflag=3"
                        json.dump(map, json_file)
                        json_file.write(",\n")
                        counts += 1
                print("已爬取" + str(counts))
        json_file.write("{}]")


