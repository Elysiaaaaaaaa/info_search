from src_sup.datastruct.InverseList import InverseList as IL
from .SkipList import SkipList as SL
class inverse_dict:
    def __init__(self):
        """
        创建词典
        :df:词频，某个单词在多少篇文章出现
        :dic: 词典，term->inversedict
        """
        self.dic = dict()
        self.df = dict()

    def __getitem__(self, term):
        """
        词元->倒排表
        :param term
        :return: inverselist
        """
        return self.dic.get(term,None)

    def add_term(self, doc_id, term, term_idx=None, tf=0):
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
            self.dic[term] = IL()
            self.df[term] = 0

        self.dic[term].insert(doc_id, term_idx, tf)
        self.df[term] += 1

    def tf(self,term):
        """
        词项频率
        :param term:
        :return: int 词频
        """
        return self.df.get(term,1e9)


    def intersection(self, terms):
        """
        查找与term相关的文章
        并集
        :param terms: 由term组成的list  [term1,term2,term3]
        :return: doc_ids    [doc_id1,doc_id2,doc_id3]
        """
        # 根据词频升序排列
        tmp_skiplist = SL()
        terms.sort(key=lambda x: self.tf(x))
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
