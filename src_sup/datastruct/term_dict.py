# from src_sup.datastruct.SkipList import Inverted_List as sl
# import re
# import os
#
# class term_dict:
#     def __init__(self):
#         """
#         创建词典
#         :param terms: 字典，作为term->skiplist
#         :term: 某个单词
#         :skiplist: 跳跃表，用于快速查找某个词
#
#         :df:词频，某个单词在多少篇文章出现
#             :tf:词项频率，某个单词在某个文章出现了多少次
#         :first: 第一篇文章出现某个词的位置
#         word:词表，收录所有term
#         dic: 词典，term->skiplist
#         """
#         self.dic = dict()
#         self.df = dict()
#         self.first = dict()
#         self.doc_id = set()
#         self.word = set()
#
#     def __getitem__(self, term):
#         """
#         词元->跳跃表
#         :param term
#         :return: skiplist
#         """
#         if term not in self.dic:
#             raise KeyError('not such term that', term)
#         else:
#             return self.dic[term]
#
#     def _read_file(self,path):
#         with open(path,'r') as f:
#             text = f.read()
#         # text = text.replace(' ','')
#         return text
#
#     def term_iter(self, word, k, sep=False):
#         """
#         词项迭代器
#         :param word:str
#         :return:
#         """
#         if sep:
#             # 处理连字符
#             word = '\t' + word + '\t'
#             word = word.split('.')
#
#             for wor in word:
#                 for i in range(len(wor) - k + 1):
#                     te = wor[i:i + k]
#                     yield te
#         else:
#             # 处理文本，直接分割
#             word = word.split()
#             for wor in word:
#                 wor = '\t' + wor + '\t'
#                 for i in range(len(wor) - k + 1):
#                     te = wor[i:i + k]
#                     yield te
#
#
#     def add_term(self, doc_id, term, word_):
#         """
#         添加词项
#         :param word_: 文档
#         :param doc_id: 文章id
#         :param term: 词
#         :param term_idx: 词在文章中的位置
#         :param cnt: 词在文章中的出现次数
#         """
#         if term not in self.word:
#             """
#             如果词不在词典中，则创建跳跃表
#             """
#             self.dic[term] = [sl()]
#             self.df[term] = 0
#             self.word.add(term)
#             self.doc_id.add(doc_id)
#         cnt = word_.count(term)
#         # 位置信息
#         term_idx = []
#         for idx in range(len(word_)):
#             # 寻找term所有出现位置
#             if word_[idx] == term:
#                 term_idx.append(idx)
#         self.dic[term].skip_insert(doc_id, term_idx, cnt)
#         self.df[term] += 1
#
#     def tf(self, term):
#         """
#         词项频率
#         :param term:
#         :return: int 词频
#         """
#         return self.df.get(term, 1e9)
#
#     def first(self, term):
#         """
#         第一篇文章出现某个词的位置
#         :param term:
#         :return: int 位置
#         """
#         return self.first[term]
#
#     def td_label_creat(self, term):
#         """
#         创建包含定term的文章下标list
#         :param term:
#         :return:
#         """
#         ls = []
#         if term not in self.dic:
#             return ls
#         slh = self.dic[term]._header.forward[0]
#         while slh is not None:
#             ls.append(slh.doc_id)
#             slh = slh.forward[0]
#         return ls
#
#     def td_intersection_kgram(self, terms, k):
#         """
#         kgram算法
#         查找与term相关的文章
#         并集
#         :param terms: 由term组成的list  [term1,term2,term3]
#         :return: doc_ids    [doc_id1,doc_id2,doc_id3]
#         """
#         fi_term = []
#         for term in terms:
#             fi_term += list(self.term_iter(term, k, sep=True))
#         ans = self.td_intersection(fi_term)
#         fi_ans = []
#         print('ans',ans)
#         # 后过滤
#         for an in ans:
#             text = self._read_file(os.path.join('../data',str(an)))
#             flag = True
#             for term in terms:
#                 if not re.search(term,text):
#                     flag = False
#                     break
#             if flag:
#                 fi_ans.append(an)
#         return fi_ans
#
#     def td_intersection(self, terms):
#         """
#         查找与term相关的文章
#         并集
#         :param terms: 由term组成的list  [term1,term2,term3]
#         :return: doc_ids    [doc_id1,doc_id2,doc_id3]
#         """
#         # 根据词频升序排列
#         terms.sort(key=lambda x: self.tf(x))
#         # 基于词频最少的term建立中间结果
#         tmp_ans = self.td_label_creat(terms[0])
#         for term in terms[1:]:
#             if tmp_ans == []:
#                 return []
#             # 处理每个布尔查询元素，判断中间结果中每一个doc_id对应的文档是否存在term
#             sl = self.dic.get(term,None)
#             if sl == None:
#                 return []
#             new_ans = []
#             for ans in tmp_ans:
#                 if sl.skip_search(ans) is not None:
#                     new_ans.append(ans)
#             tmp_ans = new_ans
#         return tmp_ans
#
#
#     def td_union_kgram(self, terms, k):
#         """
#         查找与term相关的文章
#         交集
#         通配符
#         :param terms: 由term组成的list  [term1,term2,term3]
#         :return: doc_ids    [doc_id1,doc_id2,doc_id3]
#         :param terms:
#         :param k:
#         :return:
#         """
#         ans = set()
#         for term in terms:
#             ans = ans.union(self.td_union(list(self.term_iter(term, k, sep=True))))
#         print('ans',ans)
#         fi_ans = set()
#         for an in ans:
#             text = self._read_file(os.path.join('../data',str(an)))
#             flag = False
#             for term in terms:
#                 # patt = '*'
#                 if re.search(term,text) is not None:
#                     flag = True
#                     break
#             if flag:
#                 fi_ans.add(an)
#         return fi_ans
#
#     def td_union(self, terms):
#         """
#         查找与term相关的文章
#         交集
#         :param terms: 由term组成的list  [term1,term2,term3]
#         :return: doc_ids    [doc_id1,doc_id2,doc_id3]
#         """
#         tmp_ans = set()
#         for term in terms:
#             # 处理每个布尔查询元素
#             tmp_ans = tmp_ans.union(self.td_label_creat(term))
#         return tmp_ans
#
#
#     def td_except_kgram(self, term1, term2, k):
#         """
#         查找与term相关的文章
#         差集，term1-term2
#         通配符
#         :param term1:
#         :param term2:
#         :return:
#         """
#         ans = set()
#         ans =   set(
#                     self.td_intersection(
#                         list(
#                             self.term_iter(term1, k, sep=True)
#                             )
#                         )
#                     ).difference(
#                 set(
#                     self.td_intersection(
#                         list(
#                             self.term_iter(term2, k, sep=True)
#                             )
#                         )
#                     )
#                 )
#         fi_ans = list()
#         print('ans',ans)
#         for an in ans:
#             text = self._read_file(os.path.join('../data',str(an)))
#             flag = True
#             for term in term1:
#                 if not re.search(term,text):
#                     flag = False
#                     break
#             if flag:
#                 fi_ans.append(an)
#         print('fi_ans',fi_ans)
#
#         fii_ans =[]
#         for an in fi_ans:
#             text = self._read_file(os.path.join('../data',str(an)))
#             flag = True
#             for term in term2:
#                 if re.search(term, text):
#                     print(term,text)
#                     flag = False
#                     break
#             if flag:
#                 fii_ans.append(an)
#         return fii_ans
#
#     def td_except(self, term1, term2):
#         """
#         查找与term相关的文章
#         差集，term1-term2
#         """
#         tmp_ans1 = set(self.td_label_creat(term1))
#         tmp_ans2 = set(self.td_label_creat(term2))
#         ans = tmp_ans1.difference(tmp_ans2)
#         return ans
