import os.path
from math import log,sqrt
from src.datastruct.InverseList import InverseList as IL
from .SkipList import SkipList as SL
path = 'D:\桌面\info_search\data'

class array:
    def __init__(self):
        self.dim = 0
        self.arr = dict()

    def __setitem__(self, key, value):
        self.arr[key] = value

    def __getitem__(self, item):
        return self.arr.get(item,0)

    def __len__(self):
        ans = 0
        for v in self.arr.values():
            ans += v**2
        return sqrt(ans)

    def l(self):
        ans = 0
        for v in self.arr.values():
            ans += v ** 2
        return sqrt(ans)

    def get_term(self):
        return set(self.arr.keys())

    def sim(self,other):
        terms = self.get_term()
        terms = terms.union(other.get_term())
        ans = 0
        for term in terms:
            ans += self[term] * other[term]
        ans = ans / (self.l() * other.l())
        return ans


class inverse_dict:
    def __init__(self):
        """
        创建词典
        :df:词频，某个单词在多少篇文章出现
        """
        self.dic = dict()
        self.df = dict()
        self.N = 0

    def __getitem__(self, term):
        """
        词元->倒排表
        :param term
        :return: inverselist
        """
        return self.dic.get(term,None)

    def add_term(self, doc_id, term, tf, term_idx=None):
        """
        添加词项
        :param doc_id: 文章id
        :param term: 词
        :param term_idx: 词在文章中的位置
        :param tf: 词在文章中的出现次数
        """
        if term not in self.dic:
            """
            如果词不在词典中，则创建跳跃表
            """
            self.dic[term] = IL(term)
            self.df[term] = 0

        self.dic[term].insert(doc_id, term_idx, tf)
        self.df[term] += 1
        self.N = max(self.N, doc_id)

    def tf_idf_array(self, terms):
        tmp_ans = self.intersection(terms)
        term_arr = array()
        # 计算查询向量
        for term in set(terms):
            tf = terms.count(term)
            term_arr[term] = tf
        fin_sim = dict()
        for doc_id in tmp_ans:
            doc_arr = array()
            with open(os.path.join(path,str(doc_id)),'r') as f:
                text = f.read().split()
            for text_term in set(text):
                tf = text.count(text_term)
                doc_arr[text_term] = tf
            fin_sim[doc_id] = term_arr.sim(doc_arr)
        tmp_ans = list(tmp_ans)
        tmp_ans.sort(key=lambda x: fin_sim[x], reverse=True)
        # tmp_ans = list(tmp_ans).sort(key = lambda x:fin_sim[x],reverse=True)
        return tmp_ans,fin_sim

    def tf_idf(self, terms):
        tmp_ans = self.intersection(terms)
        score = dict()
        for doc_id in tmp_ans:
            with open(os.path.join(path,str(doc_id)),'r') as f:
                text = f.read()
            for term in terms:
                tf = text.count(term)
                score[doc_id] = score.get(doc_id,0) + (1 + log(tf)) * log(self.N/self.df[term])
        tmp_ans = list(tmp_ans)
        tmp_ans.sort(key = lambda x:score[x],reverse=True)
        return tmp_ans,score

    def intersection(self, terms):
        """
        查找与term相关的文章
        并集
        :param terms: 由term组成的list  [term1,term2,term3]
        :return: doc_ids    [doc_id1,doc_id2,doc_id3]
        """
        # 根据词频升序排列
        tmp_skiplist = SL()
        terms.sort(key=lambda x: self.df.get(x,1e9))
        tmp_ans = self.dic.get(terms[0],None)
        if tmp_ans is None:
            return set()
        tmp_ans = tmp_ans.to_set()
        for ans_id in tmp_ans:
            tmp_skiplist.skip_insert(ans_id,0,0)
        for term in terms[1:]:
            # 处理每个布尔查询元素
            ter = self.dic.get(term,None)
            if ter is not None:
                tmp_ans = ter.to_set()
                skiplist = SL()
                for ans_id in tmp_ans:
                    if tmp_skiplist.skip_search(ans_id):
                        skiplist.skip_insert(ans_id,0,0)
                tmp_skiplist = skiplist
            else:
                break
        return tmp_skiplist.to_set()

    def union(self,terms):
        """
        查找与term相关的文章
        交集
        :param terms: 由term组成的list  [term1,term2,term3]
        :return: doc_ids    [doc_id1,doc_id2,doc_id3]
        """
        tmp_ans = set()
        for term in terms:
            # 处理每个布尔查询元素
            ter = self.dic.get(term,None)
            if ter is not None:
                tmp_ans = tmp_ans.union(ter.to_set())
        return tmp_ans

    def excepts(self,term1,term2):
        """
        查找与term相关的文章
        差集，term1-term2
        """
        ter1 = self.dic.get(term1,None)
        ter2 = self.dic.get(term2,None)
        ter1 = ter1.to_set(term1)
        ter2 = ter2.to_set(term2)
        if ter2 is not None:
            ter1 = ter1.difference(ter2)
        return ter1
