from urllib import request
import os
import time
import lxml
import lxml.html
import re
import json
from urllib.parse  import urljoin
import requests
from lxml import etree
import cssselect


zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')

def zh_ex(word):
    global zh_pattern
    word = word.encode("utf8")
    match = zh_pattern.search(word)
    return match
def url_open(url):
    res = request.Request(url)  #发送请求
    res.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134") #打开网页并读取内容  使用浏览器访问
    html = request.urlopen(res,timeout = 60).read()#打开网页并读取
    return html #html里面为网页内容


def getbmName(url):
    htmlstr = url_open(url).decode("gbk") #打开网页并解码,解码为网页可读取形式（charset）
    html = etree.HTML(htmlstr) #转换成Xpath可以理解的格式
    url = html.xpath('//*[@id="dw_manage"]/ul/li/a/@href')#Xpath的使用  提取节点  找出网址
    bm = html.xpath('//*[@id="dw_manage"]/ul/li/a/text()')#Xpath的使用  找出html中的文本38个
    Url = list()
    for i in range(len(bm)):
        Url.append("http://www.haikou.gov.cn/zfdt/ztbd/2016nzt/qlzrqd" + url[i][1:])  #url[i][1:]) 为url里的部门
    return [bm,Url]

def getpage(url):
    html = url_open(url).decode("gbk")
    html = etree.HTML(html)
    pagef = html.xpath('//*[@id="page_manage"]/script/text()')
    page = re.search(r'\([0-9]{1,3}',pagef[0]).group()[1:]  #提取页码
    pages = list()
    for i in range(int(page)):
        if i == 0:
            pages.append('index.html')
        else:
            pages.append('index_'+str(i)+'.html')
    return pages  #只有页码

def geturllist(urL):  #意义得到中间页的网址
    htmlstr = url_open(urL).decode("gbk")
    html = etree.HTML(htmlstr)
    url = html.xpath('//*[@id="sxlb_manage"]/ul/li/a/@href')
    Url = list()
    for i in range(len(url)):#中间页的URL的一部分，差域名
        Url.append(urljoin(urL , url[i]))#拼接网址
    return Url#放置拼接好的网址
def getdata(url):  #只是打开转码，无意义？？？
    htmlstr = url_open(url).decode("gbk")#打开网页并解码，得到网页源码，
    '''
    html = etree.HTML(htmlstr) #讲网页源码转换为树形结构
    data = list()
    data.append(html.xpath('//*[@id="content_k1"]/div[1]/div/table/tbody/tr[3]/td[1]/p/span/text()')[0])
    data.append(html.xpath('//*[@id="content_k1"]/div[1]/div/table/tbody/tr[3]/td[3]/p/span/text()')[0])
    data.append(html.xpath('//*[@id="content_k1"]/div[1]/div/table/tbody/tr[3]/td[6]/p/text()')[1])
    a = html.xpath('//*[@id="content_k1"]/div[1]/div/table/tbody/tr[3]/td[5]/p')
    law = ""
    for i in range(len(a)):
        print(html.xpath('//*[@id="content_k1"]/div[1]/div/table/tbody/tr[3]/td[5]/p['+ str(i+1) +']//span/text()')[:])
        print("\n\n")
    data.append(law)
    for i in data:
        print(i)
    '''
    return(htmlstr)

def getbsd(sbs):
    try:
        result_law = requests.post("http://172.16.4.63:8080/intelligent/rightsApi/getLawInfo",data={"setBasisSummary": sbs})
    except:
        print("v p n   掉 了")
        result_law = requests.post("http://172.16.4.63:8080/intelligent/rightsApi/getLawInfo",data={"setBasisSummary": sbs})
    result_law_j = result_law.json()
    result = list()
    if result_law_j["state"] ==1:
        for i in range(0,len(result_law_j["result"])):
            try:
                clause = result_law_j["result"][i]["articles"][0]["clause"]
            except IndexError:
                clause = ""
            try:
                content = result_law_j["result"][i]["articles"][0]["content"]
            except IndexError:
                content = ""
            try:
                law = result_law_j["result"][i]["lawName"]
            except :
                law = ""
            result.append(
                {
                    "clause":clause,
                    "law":law,
                    "content":content
                }
            )
    return result


def gettable(data,name,url):
    pass
def main():
    rightNo = 0
    os.chdir('C:/Users/ASUS/Desktop/')# 设置系统路径
    with open("海口1.json","w",encoding = "utf-8") as json_file: #打开文件"海口1.json"
        json_file.write("[\n")  #以"[\n" 的格式存储
        url = "http://www.haikou.gov.cn/zfdt/ztbd/2016nzt/qlzrqd/"  #网址
        urllist = getbmName(url) #获取部门名称
        for i in range(len(urllist[1])): #i为网址   部门循环
            page = getpage(urllist[1][i])  #得到这些网址的页码
            for j in page: #页码循环
                url2 = urllist[1][i] + j   #生成一个完整的网址
                urllist2 = geturllist(urL = url2)  #将生成的完整的网址赋予一个变量
                for k in range(len(urllist2)):
                    print(urllist2[k]) #检验
                    try:
                        data = getdata(urllist2[k])
                    except:
                        print("某原因漏了一个")
                    json.dump(data,json_file)#讲data放置到json文件中
                    json_file.write(',\n')
                    json.dump(urllist2[k],json_file)
                    json_file.write(',\n')
                    rightNo+=1
                    print(rightNo)
                print("page",j,"   to   ",len(urllist))
            print(urllist[0][i],'   完成')
        json_file.write("' '\n]")

main()

os.chdir('C:/Users/ASUS/Desktop/')
with open("海口1.json", encoding='utf-8') as f:
	table = json.load(f)  #将字符串转换为字典
f.close()
with open("海口权力清单.json", 'w', encoding='utf-8') as json_file:
    rightNo = 0
    json_file.write("[\n")
    for i in range(0,len(table)):#将所有信息采集一遍
        if i % 2 == 0:
            html = table[i]#网页内容
            url = table[i + 1]#网页网址
            print(url)#打印所有网址 html = lxml.html.fromstring(html)#等同于etree.HTML函数 print(html)
            data = html.cssselect('td')
            if len(data) == 15:
                a = data[12].text_content()
                b = data[8].text_content()
                c = data[10].text_content()
                d =data[13].text_content()
                e = html.cssselect('a')[5].text_content()
                try:
                    caseDomainDescribe = requests.post('http://172.16.4.63:8080/intelligent/rightsApi/getCaseDomain',
                                                       data={'competentDeptName': e})
                    sss = caseDomainDescribe.json()
                    caseDomainDescribe = sss['result']['industryShowName']
                    caseDomain = requests.post('http://172.16.4.63:8080/intelligent/rightsApi/getCaseDomain',
                                               data={'competentDeptName': e}).json()['result'][
                        'industryName']
                except:
                    caseDomain = ""
                    caseDomainDescribe = ""
                if a != "":
                    dic = {
                        "rightNo": rightNo,
                        "rightName": c,
                        "rightType": b,
                        "projectDecomposition": "",#项目分解
                        "executorName": d,
                        "competentDeptName": e, #####
                        "undertakingAgency": d,#主管部门
                        "jointImpDept": "",
                        "timeLimit": "",
                        "accessWay": "",
                        "complaintTel": "",
                        "undertakingUser": "",
                        "consultationTel": "",
                        "setBasisSummary": a,
                        "setBasis": a,
                        "feeBasis": "",
                        "law": "",
                        "article": "",
                        "feeScale": "",
                        "approveImpDoc": "",
                        "cityCode": '460100',  #######################################各市不同
                        "geoname": "海口市",
                        "sourceUrl": url,
                        "caseDomain": caseDomain,
                        "caseDomainDescribe": caseDomainDescribe,
                        "basisSummaryDefinition": getbsd(a),
                        "uniqueId": requests.post("http://172.16.4.63:8080/intelligent/rightsApi/getUniqid",
                                                  data={'uniqueidStr': '450100' + str(rightNo)}).json()["result"]
                    }
                    json.dump(dic, json_file)
                    json_file.write(',\n')
                    rightNo += 1#编号 有多少个权利清单，给权利清单生成编号
                    print(rightNo)
    json_file.write("' '\n]")
pass