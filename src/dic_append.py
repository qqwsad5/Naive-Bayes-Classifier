# 定义统计词频函数
def dic_append(dic,word):
    if word in dic.keys():
        dic[word] += 1
    else:
        dic[word] = 1