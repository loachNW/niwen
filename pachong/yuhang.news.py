#coding = utf-8
import os
import time
import lxml
import lxml.html
import re
import json
from urllib.parse  import urljoin
import urllib.parse
from lxml import etree
import requests
import cssselect
import urllib
import numpy as np

def get_str(url,code,method,httpmethod = "GET",FormData = None,attr = False ,ip = False):
    out = list()
    if ip:
        ip = requests.get("http://172.16.11.130:5010/get/").text
    if ip:#代理
        pass
    else:#非代理
        if httpmethod =="GET":
            res = urllib.request.Request(url)
            res.add_header("User-Agent",
                           "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
            html = urllib.request.urlopen(res, timeout=5).read()
        if httpmethod == "POST":
            data = urllib.parse.urlencode(FormData).encode('utf-8')
            html = urllib.request.urlopen(url, data).read()
    if method == "xpath":
        try:
            html = html.decode()
        except:
            html = html.decode("gbk","ignore")
        html = etree.HTML(html)
        title = html.xpath(code)
        if attr:
            for i in title:
                out.append(i.attrib[attr])
        else:
            for i in title:
                out.append(i.xpath('string(.)').strip())
    if method == "css" :
        html = lxml.html.fromstring(html)
        title = html.cssselect(code)
        if attr:
            for i in title:
                out.append(i.attib[attr])
        else:
            for i in title:
                out.append(i.text_content())
    if method =="re":
        try:
            html = html.decode()
        except:
            html = html.decode("gbk")
        out = re.findall(code,html)
    test = out[0] ####测试结果不为空，负责报错
    return out
a = requests.get("http://172.16.4.63:8080/intelligent/getRegions").json()
dic1 = {}
dic2 = {}
dic3 = {}
for i in a:
    dic1[i["abbr"].replace("省","").replace("市","").replace("区","").replace("县","")] = i["value"]
    for j in i["subs"]:
        dic2[j["abbr"].replace("市","").replace("区","").replace("县","")] = j["value"]
        for k in j["subs"]:
            dic3[k["abbr"].replace("区","").replace("县","")] = k["value"]
dic2["湘西"] = "433100"
dic2.pop('湘西，湘西州，湘西自治州')
cityName = list(dic2.keys())
def main():
    os.chdir("E:/data/新闻_市/")
    code = r'href="(http://.+?/\d+?/t\d+?_\d+?.shtml)"'
    for j in range(100,len(cityName)):
        print("城市:",cityName[j])
        num = 1
        filed = 0
        with open(cityName[j] + ".txt", "a", encoding="utf-8") as json_file:
            for i in range(2,1001):
                if filed >10:
                    break
                urllist = list()
                print("page ",i)
                url = "http://was.cnr.cn/was5/web/search?page=" + str(i) + "&channelid=234439&searchword=" + urllib.parse.quote(cityName[j]) + "&keyword=" + urllib.parse.quote(cityName[j]) + "&orderby=LIFO&was_custom_expr=%28%E6%BC%AF%E6%B2%B3%29&perpage=10&outlinepage=10&searchscope=&timescope=&timescopecolumn=&orderby=LIFO&andsen=&total=&orsen=&exclude="
                try:
                    urllist = get_str(url, code, "re", httpmethod="GET", FormData=None, attr="href", ip=False)
                except:
                    print("当前页打开失败")
                    filed +=1
                urllist = np.unique(urllist)
                for k in range(len(urllist)):
                    code1 = '//*[@class="article"]'
                    url = urllist[k]
                    try:
                        text = get_str(code=code1, url=url, method="xpath")[0].replace("\r", "").replace("\n","").replace("\u3000", "").replace("\t", "")
                        json_file.write(text + "\t" + dic2[cityName[j]]+"\n")
                        print(num)
                        num += 1
                    except:
                        print(url)
    pass
main()
