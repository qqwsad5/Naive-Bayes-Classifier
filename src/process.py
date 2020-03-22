import re
import os
from src.divide import set_divide
from src.dic_append import dic_append

# 定义文件位置
PARAMS_PATH = "../params/"
DATA_PATH = "../data/mails/"
LABEL_PATH = "../data/labels/index"

# 用于处理的正则表达式
filter_not_letter = re.compile("[^a-z|^A-Z]")
filter_spaces = re.compile(" +")

# 统计词频
ham_diction = {}
spam_diction = {}

# 打开标签文件进行处理
label_file = open(LABEL_PATH,'r')
labels = label_file.readlines()

# 分割训练集测试集
labels = set_divide(set=labels, isTrain=True)

print("总共: {}条记录".format(len(labels)))
# 记录数量
count = 0
failed = 0
ham_count = 0
spam_count = 0

for i in labels:
    # 找到条目对应的标签和文件位置
    [label,path] = i.strip().split(' ../data/')

    # 打开邮件进行处理,碰到非UTF-8编码的文件跳过
    mail_file = open(os.path.join(DATA_PATH,path),'r', encoding='UTF-8')
    try:
        lines = mail_file.readlines()
    except:
        failed += 1
        continue

    # 记录邮件数量
    if label == 'ham':
        ham_count += 1
    else:
        spam_count += 1

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
            # 根据标签放入对应的统计字典
            if label == 'ham':
                for word in words:
                    dic_append(ham_diction, word)
            else:
                for word in words:
                    dic_append(spam_diction, word)

    count += 1
    sum = count + failed
    if sum%50 == 0 or sum == len(labels):
        print("\r用于训练: {}/{}; 无法解码文件: {}/{}".format(count,len(labels),failed,len(labels)), end="")

print("\n正常邮件数：{};垃圾邮件数：{}".format(ham_count,spam_count))
print("保存中...")

# 全部用字符串保存字典
info = {"sum":count,"ham":ham_count,"spam":spam_count}
fp = open(os.path.join(PARAMS_PATH,'count'),'w')
fp.write(str(info))
fp.close()

# 正常邮件
fp = open(os.path.join(PARAMS_PATH,'ham'),'w')
fp.write(str(ham_diction))
fp.close()

# 垃圾邮件
fp = open(os.path.join(PARAMS_PATH,'spam'),'w')
fp.write(str(spam_diction))
fp.close()

print("保存完成")