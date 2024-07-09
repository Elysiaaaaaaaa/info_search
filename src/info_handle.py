import os
import tqdm
from src.datastruct.k_gram import k_gram_dict
from src.datastruct.InverseDict import inverse_dict
docs = os.listdir("../data")
main_path = r'..\data'
k_gram = 3
KGD = k_gram_dict(k_gram)
ID = inverse_dict()
pattern = r'[^\w\s]'
demo = False

docnt = 0
for doc in tqdm.tqdm(docs):
    # 处理单个文件
    docnt += 1
    if demo and docnt > 100:
        print('demo ok')
        break
    path = os.path.join(main_path, doc)
    with open(path,'r') as f:
        lines = f.readlines()
    text = ''
    for line in lines:
        text += ' ' + line
    # 去除标点
    # word = re.sub(pattern, ' ', word)
    doc_id = int(doc)
    KGD.add_text(text,doc_id)
    for term in set(text.split()):
        ID.add_term(doc_id, term, tf=text.count(term))

if not demo:
    with open(r'..\37220222203885.txt','w') as w:
        with open(r'..\query-2024.txt','r') as r:
            key_words = r.readlines()
        for key_word in key_words:
            key_word = key_word.split()
            ans = list(ID.intersection(key_word))
            for i in range(len(ans)):
                w.write(str(ans[i]))
                w.write('\t')
            w.write('\n')

print('i.并集 and')
print('u.交集 or')
print('e.差集 -')
print('ti. tfidf')
print('tac. tfidf_array_cos')
print('.i.通配符并集 and')
print('.u.通配符交集 or')
print('.e.通配符差集 -')
while True:
    tye = input()
    ans = None
    score = None
    key_word = input().split()
    flag = True
    try:
        if tye == 'i':
            ans = ID.intersection(key_word,f=True)
        elif tye == 'u':
            ans = ID.union(key_word,f=True)
        elif tye == 'e':
            ans = ID.excepts(key_word[0],key_word[1],f=True)
        elif tye == 'ti':
            ans,score = ID.tf_idf(key_word)
        elif tye == 'tia':
            ans,score = ID.tf_idf_array(key_word)
        elif tye == '.i':
            ans = KGD.intersection_kgram(key_word)
        elif tye == '.u':
            ans = KGD.union_kgram(key_word)
        elif tye == '.e':
            ans = KGD.except_kgram(key_word[0],key_word[1])
        else:
            flag = False
            print('输入错误')
        if flag:
            print("答案个数：",len(ans))
            print(ans)
            if score:
                for term in ans:
                    print(term,':',score[term])
    except Exception as e:
        print(e)