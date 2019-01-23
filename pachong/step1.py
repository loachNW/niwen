import os
import numpy as np
import random

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
    with open("E:/data/step1/" + file,"w",encoding="utf-8") as f:
        for i in table:
            f.write(i+"\n")

file1 = "E:/data/新闻_市/"
name1 = os.listdir(file1)
for i in range(len(name1)):
    table = readtxt(os.path.join(file1, name1[i]))
    rename = replace_name(table, name1[i])
    table = table + rename
    if len(table)>12000:
        table = random.sample(table,12000)
    save_content(table,name1[i])
