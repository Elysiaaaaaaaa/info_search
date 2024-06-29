from src.datastruct.SkipList import SkipList as sl


class term_dict:
    def __init__(self):
        """
        创建词典
        :param terms: 字典，作为term->skiplist
        :term: 某个单词
        :skiplist: 跳跃表，用于快速查找某个词

        :df:词频，某个单词在多少篇文章出现
            :tf:词项频率，某个单词在某个文章出现了多少次
        :first: 第一篇文章出现某个词的位置
        word:词表，收录所有term
        dic: 词典，term->skiplist
        """
        self.dic = dict()
        self.df = dict()
        self.first = dict()
        self.word = []

    def __getitem__(self, term):
        """
        词元->跳跃表
        :param term
        :return: skiplist
        """
        if term not in self.dic:
            raise KeyError('not such term that',term)
        else:
            return self.dic[term]

    def add_term(self, doc_id, term, first_idx, cnt):
        """
        添加词项
        :param doc_id: 文章id
        :param term: 词
        :param first_idx: 词在文章中的首次出现位置
        :param cnt: 词在文章中的出现次数
        """
        if term not in self.dic:
            """
            如果词不在词典中，则创建跳跃表
            """
            self.dic[term] = sl()
            self.df[term] = 0

        self.dic[term].skip_insert(doc_id, first_idx, cnt)
        self.df[term] += 1

    def tf(self,term):
        """
        词项频率
        :param term:
        :return: int 词频
        """
        return self.df.get(term,1e9)

    def first(self,term):
        """
        第一篇文章出现某个词的位置
        :param term:
        :return: int 位置
        """
        return self.first[term]

    def td_label_creat(self,term):
        """
        创建包含定term的文章下标list
        :param term:
        :return:
        """
        ls = []
        if term not in self.dic:
            return ls
        slh = self.dic[term].header.forward[0]
        while slh is not None:
            ls.append(slh.doc_id)
            slh = slh.forward[0]
        return ls

    def td_intersection(self, terms):
        """
        查找与term相关的文章
        并集
        :param terms: 由term组成的list  [term1,term2,term3]
        :return: doc_ids    [doc_id1,doc_id2,doc_id3]
        """
        # 根据词频升序排列
        terms.sort(key=lambda x: self.tf(x))
        # 基于词频最少的term建立中间结果
        tmp_ans = self.td_label_creat(terms[0])
        for term in terms[1:]:
            # 处理每个布尔查询元素，判断中间结果中每一个doc_id对应的文档是否存在term
            sl = self.dic[term]
            new_ans = []
            for ans in tmp_ans:
                if sl.skip_search(ans) is not None:
                    new_ans.append(ans)
            tmp_ans = new_ans
        return tmp_ans

    def td_union(self,terms):
        """
        查找与term相关的文章
        交集
        :param terms: 由term组成的list  [term1,term2,term3]
        :return: doc_ids    [doc_id1,doc_id2,doc_id3]
        """
        tmp_ans = set()
        for term in terms:
            # 处理每个布尔查询元素
            tmp_ans = tmp_ans.union(self.td_label_creat(term))
        return tmp_ans
    def td_except(self,term1,term2):
        """
        查找与term相关的文章
        差集，term1-term2
        """
        tmp_ans1 = set(self.td_label_creat(term1))
        tmp_ans2 = set(self.td_label_creat(term2))
        ans = tmp_ans1.difference(tmp_ans2)
        return ans