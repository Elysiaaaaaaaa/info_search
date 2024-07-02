import os
import re
import tqdm
# from src_sup.datastruct.term_dict import term_dict
from src_sup.datastruct.InverseDict import inverse_dict
docs = os.listdir("../data")
main_path = r'..\data'
k_gram = 2
ID = inverse_dict()
pattern = r'[^\w\s]'
demo = True
docnt = 0
for doc in tqdm.tqdm(docs):
    # 处理单个文件
    # docnt += 1
    # if demo and docnt > 2:
    #     print('demo ok')
    #     break
    path = os.path.join(main_path, doc)
    with open(path,'r') as f:
        texts = f.readlines()
    word = ''
    for text in texts:
        word += ' ' + text
    # 去除标点
    # word = re.sub(pattern, ' ', word)
    doc_id = int(doc)
    for term in set(word.split()):
        ID.add_term(doc_id,term,tf=word.count(term))
    # td.add_term_kgram(doc_id,word,k_gram)
# print('1')

# while True:
#     print('i.并集 and')
#     print('u.交集 or')
#     print('e.差集 -')
#     type = input()
#     key_word = input().split()
#     # try:
#     if type == 'i':
#         print(ID.td_intersection_kgram(key_word))
#         # print(td.td_intersection_kgram(key_word,k_gram))
#     elif type == 'u':
#         print(ID.td_union_kgram(key_word))
#         # print(td.td_union_kgram(key_word,k_gram))
#     elif type == 'e':
#         print(ID.td_except(key_word[0],key_word[1]))
#         # print(td.td_except_kgram(key_word[0],key_word[1],k_gram))
#     else:
#         print('输入错误')

with open(r'C:\Users\Elysia\code\python\data_search_hw\src\ans-2024.txt','w') as w:
    with open(r'C:\Users\Elysia\code\python\data_search_hw\src\query-2024.txt','r') as r:
        key_words = r.readlines()
    for key_word in key_words:
        key_word = key_word.split()
        ans = list(ID.intersection(key_word))
        for i in range(len(ans)):
            w.write(str(ans[i]))
            w.write('\t')
            # ans[i] = str(ans[i])
        # w.write(' '.join(ans))
        w.write('\n')

while True:
    print('i.并集 and')
    print('u.交集 or')
    print('e.差集 -')
    type = input()
    key_word = input().split()
    # try:
    if type == 'i':
        print(ID.intersection(key_word))
        # print(td.td_intersection_kgram(key_word,k_gram))
    elif type == 'u':
        print(ID.union(key_word))
        # print(td.td_union_kgram(key_word,k_gram))
    elif type == 'e':
        print(ID.excepts(key_word[0],key_word[1]))
        # print(td.td_except_kgram(key_word[0],key_word[1],k_gram))
    else:
        print('输入错误')