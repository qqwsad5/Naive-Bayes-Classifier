import random
# 定义参量
NUM_OF_PARTS = 5
TEST_PART = 4
# 训练集随机选取部分
PART_OF_TRAIN = 1

# 数据集划分函数
def set_divide(set, isTrain):
    assert TEST_PART in range(NUM_OF_PARTS)
    assert PART_OF_TRAIN <= 1 and PART_OF_TRAIN >= 0
    sum = len(set)
    part = int(sum/NUM_OF_PARTS)
    # 余数
    rest = sum % NUM_OF_PARTS
    # 开始位置和结束位置
    start = TEST_PART*part + min(rest,TEST_PART)
    end = start + part
    if TEST_PART<rest:
        end += 1
    if isTrain:
        train_set = set[0:start] + set[end:]
        start = random.randint(0,len(train_set))
        size = int(PART_OF_TRAIN*len(train_set))
        if start+size <= len(train_set):
            train_set = train_set[start:start+size]
        else:
            train_set = train_set[start:] + train_set[0:start+size - len(train_set)]
        return train_set
    else:
        return set[start:end]
