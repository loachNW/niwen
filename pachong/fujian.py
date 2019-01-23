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
import urllib.request
import math



def url_open(url):
    res = request.Request(url)  #发送请求
    res.add_header("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134") #打开网页并读取内容  使用浏览器访问
    aa = 1
    while 1:
        aa += 1
        html = ""
        try:
            html = request.urlopen(res, timeout=60).read()  # 打开网页并读取
        except:
            pass
            print('这个网页进不去:',url)
        if html == "" or aa > 5:
            break
    return html #html里面为网页内容



def post_id(page,areaCode): #得到主干网页内容
    url = 'http://www.fjbs.gov.cn/LiabilitiseAction.action' # 网址
    data = {}
    data['fn'] = 'getPowerList'
    data['areaCode'] = areaCode
    data['type'] = ''
    data['keyword'] = ''
    data['pageSize'] = '10'
    data['pageNum'] = page
    data = urllib.parse.urlencode(data).encode('utf-8')  # 转化data格式为
    res = request.urlopen(url, data)
    html = res.read().decode('utf-8')
    return html


def post_page(areaCode):
    url =  'http://www.fjbs.gov.cn/LiabilitiseAction.action'
    data = {}
    data['fn'] = 'getPowerList'
    data['areaCode'] = areaCode
    data['type'] = ''
    data['keyword'] = ''
    data['pageSize'] = '10'
    data['pageNum'] = '1'
    data = urllib.parse.urlencode(data).encode('utf-8')
    res = request.urlopen(url, data)
    htmlstr = res.read().decode('utf-8')
    html = re.findall(r'"totalCount":(\d+?),"',htmlstr)
    page = math.ceil(int(html[0])/10)
    return(page)



def post_main_id(page,areaCode):
    url = 'http://www.fjbs.gov.cn/LiabilitiseAction.action'
    data = {}
    data['fn'] = 'getPowerList'
    data['areaCode'] = areaCode
    data['type'] = ''
    data['keyword'] = ''
    data['pageSize'] = '10'
    data['pageNum'] = page
    data = urllib.parse.urlencode(data).encode('utf-8')
    res = request.urlopen(url, data)
    htmlstr = res.read().decode('utf-8')
    main_unid = re.findall(r'"UNID":"(.+?)"',htmlstr )
    main_name = re.findall(r'"LIABILITISENAME":"(.+?)"',htmlstr)
    return(main_unid,main_name)




def post_Branch_id(areaCode,main_unid):#分支id
    url = 'http://www.fjbs.gov.cn/LiabilitiseAction.action'
    data = {}
    data['fn'] = 'getPowerSubByNameOther'
    data['areaCode'] = areaCode
    data['keyword'] = ''
    data['powerunids'] = main_unid
    data['stype'] = ''
    data = urllib.parse.urlencode(data).encode('utf-8')
    res = request.urlopen(url, data)
    htmlstr = res.read().decode('utf-8')
    return(htmlstr)


def arecode(url):#收集arecode
    htmlstr = url_open(url).decode("utf-8") # 打开网页并解码,解码为网页可读取形式（charset）
    html = etree.HTML(htmlstr)  # 转换成Xpath可以理解的格式
    arecode_id = html.xpath('//*[@id="deptDataList"]/li/@id')  # Xpath的使用  提取节点  找出网址
    for i in range(len(arecode_id)):
        arecode_id[i] = arecode_id[i][5:]
    return(arecode_id)

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





def turn(li):
    out = ""
    for i in li:
        out = out +i +","
    return out[:-2]



def main():
    rightNo = 0
    rightType_2 = ["行政许可", "行政处罚", "行政强制", "行政征收", "行政裁决", "行政确认", "行政给付", "行政奖励", "行政检查", '行政服务' ,'内部审批','其他职责事项', '行政征用',"其他行政权力"]
    rightType_code = ['XK', 'CF','QZ','ZS','CJ', 'QR', 'GF','JL', 'JC','FW', 'NS', 'QL', 'ZY', 'QT']
    rightcode = {}
    for i in range(14):
        rightcode[rightType_code[i]] = rightType_2[i]
    os.chdir('C:/Users/ASUS/Desktop/')# 设置系统路径
    with open("福建2.json","w",encoding = "utf-8") as json_file: #打开文件"海口1.json"
        json_file.write("[\n")  #以"[\n" 的格式存储
        url = 'http://www.fjbs.gov.cn/LiabilitiseAction.action'
        arecode_id = arecode(url)
        for i in range(11,len(arecode_id)):#i为每个arecode
            pages = post_page(arecode_id[i])#得到页码
            for page in range(pages):
                main_list = post_main_id(page, arecode_id[i])
                for k in range(len(main_list[0])):
                    if main_list[1][k] == "\",":
                        continue
                    main_url = 'http://www.fjbs.gov.cn/LiabilitiseAction.action?fn=getPowerDetail&powerunid=' + main_list[0][k]
                    html_1 = url_open(main_url).decode('utf-8')#得到主干内容
                    html_1 = lxml.html.fromstring(html_1)  # 等同于etree.HTML函数
                    data = html_1.cssselect('td')
                    rightname = main_list[1][k]
                    rightType = data[78 - 16].text_content()
                    executorName = data[84 - 16].text_content()
                    setBasis = data[88 - 16].text_content()
                    sourceUrl = main_url
                    setBasisSummary = data[88 - 16].text_content()
                    try:
                        aa = requests.post('http://172.16.4.63:8080/intelligent/rightsApi/getCaseDomain',
                                           data={'competentDeptName': executorName}).json()
                        caseDomainDescribe = aa['result']['industryShowName']
                        caseDomain = aa['result']['industryName']
                    except:
                        caseDomain = ""
                        caseDomainDescribe = ""
                    dic = {
                        "rightNo": str(rightNo).zfill(4),
                        "rightName": rightname,
                        "rightType": rightType,
                        "projectDecomposition": "",
                        "executorName": executorName,
                        "competentDeptName": '',  #####
                        "undertakingAgency": "",  # 承办机构
                        "jointImpDept": "",
                        "timeLimit": "",
                        "accessWay": "",
                        "complaintTel": "",
                        "undertakingUser": "",
                        "consultationTel": "",
                        "setBasisSummary": setBasisSummary,
                        "setBasis":setBasis,
                        "feeBasis": "",
                        "law": "",
                        "article": "",
                        "feeScale": "",
                        "approveImpDoc": "",
                        "cityCode": "350000",  #######################################各市不同
                        "geoname": "福建",
                        "sourceUrl": sourceUrl,
                        "caseDomain": caseDomain,
                        "caseDomainDescribe": caseDomainDescribe,
                        "basisSummaryDefinition": getbsd(setBasis),
                        "uniqueId": str(requests.post("http://172.16.4.63:8080/intelligent/rightsApi/getUniqid",
                                                      data={'uniqueidStr': "350000" + str(rightNo).zfill(4)}).json()[
                                            "result"])
                    }
                    json.dump(dic, json_file)  # 讲data放置到json文件中
                    json_file.write(',\n')
                    rightNo += 1
                    print(rightNo,main_url)
                main_unid = turn(main_list[0])
                html_2 = post_Branch_id(arecode_id[i], main_unid)  # 得到所有枝干网页内容
                Branch_unid = re.findall(r'"UNID":"(.+?){0,1}"', html_2)
                setBasisSummary = re.findall(r'"ACCORDING":"(.+?){0,1}","', html_2)
                citycode = re.findall(r'"DEPTCODE":"(\d+?){0,1}"', html_2)
                executorName = re.findall(r'"EXECUTORCOMMON":"(.+?){0,1}"', html_2)
                competentDeptName = re.findall(r'"DEPTNAME":"(.+?){0,1}"', html_2)
                rightType = re.findall(r'"STYPE":"(\w+?){0,1}"', html_2)
                rightName = re.findall(r'"SUBNAME":"(.+?){0,1}","', html_2)
                for z in range(len(Branch_unid)):
                    if rightName[z] == "\",":
                        continue
                    try:
                        aa = requests.post('http://172.16.4.63:8080/intelligent/rightsApi/getCaseDomain',
                                           data={'competentDeptName': executorName}).json()
                        caseDomainDescribe = aa['result']['industryShowName']
                        caseDomain = aa['result']['industryName']
                    except:
                        caseDomain = ""
                        caseDomainDescribe = ""
                    dic = {
                        "rightNo": str(rightNo).zfill(4),
                        "rightName": rightname,
                        "rightType": rightcode[rightType[z]],
                        "projectDecomposition": "",
                        "executorName": executorName[z],
                        "competentDeptName": competentDeptName[z],  #####
                        "undertakingAgency": "",  # 承办机构
                        "jointImpDept": "",
                        "timeLimit": "",
                        "accessWay": "",
                        "complaintTel": "",
                        "undertakingUser": "",
                        "consultationTel": "",
                        "setBasisSummary": setBasisSummary[z],
                        "setBasis":setBasisSummary[z],
                        "feeBasis": "",
                        "law": "",
                        "article": "",
                        "feeScale": "",
                        "approveImpDoc": "",
                        "cityCode": 350000,  #######################################各市不同
                        "geoname": "福建",
                        "sourceUrl":'http://www.fjbs.gov.cn/LiabilitiseAction.action?fn=getPowerDetail&powerunid=' + Branch_unid[z],
                        "caseDomain": caseDomain,
                        "caseDomainDescribe": caseDomainDescribe,
                        "basisSummaryDefinition": getbsd(setBasis),
                        "uniqueId": str(requests.post("http://172.16.4.63:8080/intelligent/rightsApi/getUniqid",
                                                      data={'uniqueidStr': "350000" + str(rightNo).zfill(4)}).json()[
                                            "result"])
                    }
                    if dic["executorName"] == "\",":
                        dic["executorName"] = ""
                    json.dump(dic, json_file)  # 讲data放置到json文件中
                    json_file.write(',\n')
                    rightNo += 1
                    print(rightNo,main_url)
        json_file.write("' '\n]")
main()
