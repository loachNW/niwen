import collections

train = open("E:/data/lix/train.txt", 'r', encoding='utf-8')
label = open("E:/data/lix/label.txt", 'r', encoding='utf-8')
f = open('train_unique.txt',"w",encoding="utf-8")
g = open('lable_unique.txt',"w",encoding="utf-8")
counts = 1
id = []
for t,l in zip(train,label):
    if counts %1000 ==0:
        print (counts)
    if t not in id:
        id.append(t)
        f.write(t)
        g.write(l)
    counts += 1

f.close()
g.close()