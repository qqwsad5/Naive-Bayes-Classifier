import re
import os
import math
from src.divide import set_divide
from src.dic_append import dic_append

# 平滑参数
EPSILON = 10

# 定义文件位置
PARAMS_PATH = "../params/"
DATA_PATH = "../data/mails/"
LABEL_PATH = "../data/labels/index"

print("读取中...")
# 全部用字符串保存字典
fp = open(os.path.join(PARAMS_PATH,'count'),'r')
info = eval(fp.read())
fp.close()

# 正常邮件
fp = open(os.path.join(PARAMS_PATH,'ham'),'r')
ham_diction = eval(fp.read())
fp.close()
ham_sum = 0
for i in ham_diction.values():
    ham_sum += i

# 垃圾邮件
fp = open(os.path.join(PARAMS_PATH,'spam'),'r')
spam_diction = eval(fp.read())
fp.close()
spam_sum = 0
for i in spam_diction.values():
    spam_sum += i

print("读取完成")

# 用于处理的正则表达式
filter_not_letter = re.compile("[^a-z|^A-Z]")
filter_spaces = re.compile(" +")

# 打开标签文件进行处理
label_file = open(LABEL_PATH,'r')
labels = label_file.readlines()

# 分割训练集测试集
labels = set_divide(set=labels, isTrain=False)

print("总共: {}条记录".format(len(labels)))
# 记录数量
ham_correct = 0
ham_wrong = 0
spam_correct = 0
spam_wrong = 0

for i in labels:
    # 找到条目对应的标签和文件位置
    [label,path] = i.strip().split(' ../data/')

    # 打开邮件进行处理
    mail_file = open(os.path.join(DATA_PATH,path),'r', encoding='UTF-8')
    try:
        lines = mail_file.readlines()
    except:
        continue

    # 统计词频
    diction = {}

    for line in lines:
        # 删去空行
        line = line.strip()
        if len(line) > 0:
            # # 只取部分特征
            # choose = line.split(':')
            # if "From" not in choose or len(choose) != 2:
            #     continue
            # else:
            #     text = choose[1]

            # 只取大小写字母组成的单词
            text = filter_not_letter.sub(" ", line)
            text = filter_spaces.sub(" ", text)
            words = text.split(' ')
            # 统计字典
            for word in words:
                dic_append(diction, word)

    # 计算邮件判断得分
    ham_value = math.log(info["ham"] / info["sum"])
    spam_value = math.log(info["spam"] / info["sum"])
    for word in diction.keys():
        # 平滑处理
        if word in ham_diction.keys():
            ham_value += diction[word]*math.log((ham_diction[word] + EPSILON) / (ham_sum + EPSILON))
        else:
            ham_value += diction[word] * math.log(EPSILON / (ham_sum + EPSILON))
        if word in spam_diction.keys():
            spam_value += diction[word] * math.log((spam_diction[word] + EPSILON) / (spam_sum + EPSILON))
        else:
            spam_value += diction[word] * math.log(EPSILON / (spam_sum + EPSILON))

    # 统计
    if ham_value>spam_value:
        if label == 'ham':
            ham_correct += 1
        else:
            spam_wrong += 1
    else:
        if label == 'spam':
            spam_correct += 1
        else:
            ham_wrong += 1

print("测试完成")
print("{}/{}".format(ham_correct, ham_correct+ham_wrong, 100*ham_correct/(ham_correct+ham_wrong)))
print("{}/{}".format(ham_wrong, ham_correct+ham_wrong, 100*ham_wrong/(ham_correct+ham_wrong)))
print("{}/{}".format(spam_correct, spam_correct+spam_wrong, 100*spam_correct/(spam_correct+spam_wrong)))
print("{}/{}".format(spam_wrong, spam_correct+spam_wrong, 100*spam_wrong/(spam_correct+spam_wrong)))
print("{:.2f}%".format(
                                   100*(ham_correct+spam_correct)/(ham_correct+ham_wrong+spam_correct+spam_wrong)))