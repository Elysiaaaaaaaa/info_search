import os
import re
import tqdm
from src.datastruct.term_dict import term_dict
docs = os.listdir("../data")
main_path = r'..\data'
td = term_dict()
pattern = r'[^\w\s]'
for doc in tqdm.tqdm(docs):
    # 处理单个文件
    if int(doc) > 6000:
        os.remove(os.path.join(main_path, doc))