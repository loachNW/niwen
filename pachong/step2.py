import os
import numpy as np
import random
import requests

def readtxt(file):
    with open(file,encoding="utf-8") as content:
        table = content.read()
    table = table.split("\n")[:-1]
    return table

def replace_name(table,name):
    out = []
    name = name[:-4]
    id = random.sample(range(len(table)),int(len(table)/5))
    for i in id:
        out.append(table[i].replace(name,"的"))
    return(out)

def save_content(table,file):
    code = dic2[file[:-4]]
    with open("E:/data/step1/" + file,"w",encoding="utf-8") as f:
        for i in table:
            f.write(i.split("\t")[0]+'\t'+code+'\n')
a = requests.get("http://172.16.11.36:8080/intelligent/getRegions").json()
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
file1 = "E:/data/step1/"
file2 = "E:/data/step2/"
try:
    os.makedirs(file2)
except:
    pass
name1 = os.listdir(file1)
with open("E:/data/step2/all_city.txt","w",encoding="utf-8") as f:
    for i in range(len(name1)):
        code = dic2[name1[i][:-4]]
        table = readtxt(os.path.join(file1, name1[i]))
        for i in table:
            f.write(i.split("\t")[0] + '\t' + code + '\n')

