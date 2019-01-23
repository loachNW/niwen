from selenium import webdriver
from urllib import request
import os
import time
import lxml
import lxml.html
import re
import json
from urllib.parse import urljoin
from lxml import etree
import requests
import cssselect
import numpy as np
import urllib


def url_open(url):
    res = request.Request(url)
    res.add_header("User-Agent",
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134")
    html = request.urlopen(res, timeout=5).read()
    return html


def open_Explor():
    # options = webdriver.ChromeOptions()
    # options.add_argument('headless')
    # driver = webdriver.Chrome(chrome_options=options)
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver


def findBycss(url, css):
    html = url_open(url).decode("gbk")
    html = lxml.html.fromstring(html)
    try:
        data = html.cssselect(css)[0]
    except:
        try:
            data = html.cssselect(".artDet")[0]
        except:
            try:
                data = html.cssselect(".show_text")[0]
            except:
                try:
                    data = html.cssselect(".box_text")[0]
                except:
                    data = html.cssselect("#p_content")[0]
    out = data.text_content()
    return out


def main():
    dirver = open_Explor()
    os.chdir("C:\\Users\\Administrator\\Desktop\\fff")
    for k in range(258,300):
        print("城市：",cityName[k],k)
        with open(cityName[k] + ".txt", "a", encoding="utf-8") as json_file:
            for i in range(1, 1001):
                print("page:",i)
                url = "http://search.people.com.cn/cnpeople/search.do?pageNum=" + str(i) + "&keyword=" +urllib.parse.quote(cityName[k].encode("gb2312")) + "&siteName=news&facetFlag=true&nodeType=belongsId&nodeId=0"
                while 1:
                    print("try!")
                    dirver.get(url)
                    html = dirver.page_source
                    if "没有符合条件" not in html and "HTTP Status 500" not in html:
                        break
                id = dirver.find_elements_by_xpath('/html/body/div[3]/div[2]/ul/li[1]/b/a')
                for j in id:
                    try:
                        content = findBycss(j.get_attribute("href"), '.box_con').replace("\r", "").replace("\n","").replace("\u3000", "").replace("\t", "")
                        json_file.write(content + "\t" + dic2[cityName[k]] + "\n")
                    except:
                        print(j.get_attribute("href"))
a = requests.get("http://172.16.11.36:8080/intelligent/getRegions").json()
dic1 = {}
dic2 = {}
dic3 = {}
for i in a:
    dic1[i["abbr"].replace("省","").replace("市","").replace("区","").replace("县","")] = i["value"]
    for j in i["subs"]:
        dic2[j["abbr"]] = j["value"]
        for k in j["subs"]:
            dic3[k["abbr"].replace("区","").replace("县","")] = k["value"]
dic2["湘西"] = "433100"
dic2.pop('湘西，湘西州，湘西自治州')
cityName = list(dic2.keys())

main()