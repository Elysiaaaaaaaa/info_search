import os
import re
import tqdm
from src.datastruct.term_dict import term_dict
docs = os.listdir("../data")
main_path = r'..\data'
td = term_dict()
pattern = r'[^\w\s]'
demo = True
docnt = 0
for doc in tqdm.tqdm(docs):
    # 处理单个文件
    docnt += 1
    if demo and docnt > 500:
        print('demo ok')
        break
    path = os.path.join(main_path, doc)
    with open(path,'r') as f:
        texts = f.readlines()
    word = ''
    for text in texts:
        word += ' ' + text
    # 去除标点
    # word = re.sub(pattern, ' ', word)
    word_ = list(word.split())
    # print(doc,word_)
    for term in word_:
        # 处理每个term
        cnt = word.count(term)
        first_idx = word.index(term)
        doc_id = int(doc)
        td.add_term(doc_id,term,first_idx,cnt)
print('1')

while True:
    print('i.并集 and')
    print('u.交集 or')
    print('e.差集 -')
    type = input()
    key_word = input().split()
    # try:
    if type == 'i':
        print(td.td_intersection(key_word))
    elif type == 'u':
        print(td.td_union(key_word))
    elif type == 'e':
        print(td.td_intersection(key_word))
    else:
        print('输入错误')