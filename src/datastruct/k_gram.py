from src.datastruct.InverseDict import inverse_dict as ID
import re

class _k_gram:
    def __init__(self, k_gram):
        self.k_gram = k_gram
        self.term_dict = ID()


class k_gram_dict:
    """
    通配符
    """
    def __init__(self, k):
        # 实现k_gram --> inverse_dict映射
        self.k_gram_dict = dict()
        # 分割长度
        self.k = k

    def __len__(self):
        return len(self.k_gram_dict)

    def __getitem__(self, item):
        return self.k_gram_dict[item]

    def add_text(self, text, doc_id):
        """
        直接将输入的文本存储
        :param text: str
        :param doc_id: int
        :return:
        """
        terms = text.split()
        for term in set(terms):
            self.add_term(term, doc_id, text)

    def add_term(self, term, doc_id, text):
        """
        添加词项，不考虑通配符
        :param terms:
        :param doc_id:
        :param text:
        :return:
        """
        terms = '\t' + term + '\t'
        for i in range(len(terms) - self.k + 1):
            k_gram = terms[i:i + self.k]
            if k_gram not in self.k_gram_dict:
                self.k_gram_dict[k_gram] = _k_gram(self.k)
            tf = text.count(k_gram)
            self.k_gram_dict[k_gram].term_dict.add_term(doc_id, term, tf=tf, term_idx=0)

    def jaccard(self, tim, term1_cnt, term2):
        return tim / (term1_cnt + len(term2) - self.k*2 + 2 - tim)

    def k_gram_handle(self, k_gram, J=0.5):
        """
        处理正则+拼写矫正
        :param k_gram:
        :param J:
        :return:
        """
        assert isinstance(k_gram, str)
        k_gram_ = '\t' + k_gram + '\t'
        k_gram_ = k_gram_.split('.')
        cnt = 0
        term = set()
        term_time = dict()
        term_docid = dict()
        for k_gra in k_gram_:
            cnt += len(k_gra) + 1 - self.k
            for i in range(len(k_gra) - self.k + 1):
                # 对分离出通配符后的查询处理 and
                k_gr = k_gra[i:i + self.k]
                if k_gr not in self.k_gram_dict:
                    return None
                else:
                    terms = self.k_gram_dict[k_gr].term_dict.dic
                    for t in terms:
                        # 出现次数
                        term_time[t] = term_time.get(t,0) + 1
                        if term_time[t] == 1:
                            # 单词对应文档
                            term_docid[t] = self.k_gram_dict[k_gr].term_dict.dic[t].nodes
                    # if term is None:
                    #     term = self.k_gram_dict[k_gr].term_dict.doc_id.copy()
                    # else:
                    #     tmp = self.k_gram_dict[k_gr].term_dict.doc_id
                    #     term = term.intersection(tmp)
        ans = set()
        for k, v in term_time.items():
            j = self.jaccard(v,cnt,k)
            if j > J:
                for kt in term_docid[k]:
                    ans.add(kt.doc_id)
        return ans
        # 后过滤 此处是完全匹配
        # fi_ans = set()
        # for pos_ans in ans:
        #     if re.search(k_gram, pos_ans) is not None:
        #         fi_ans.add(pos_ans)
        # return fi_ans

    def intersection_kgram(self, terms):
        """

        :param terms: list
        :return:
        """
        ans = None
        for term in terms:
            if ans is None:
                ans = self.k_gram_handle(term)
            else:
                ans = ans.intersection(self.k_gram_handle(term))
            if ans is None:
                return None
        return ans

    def union_kgram(self, terms):
        """

        :param terms: list
        :return:
        """
        ans = None
        for term in terms:
            if ans is None:
                ans = self.k_gram_handle(term)
            else:
                ans = ans.union(self.k_gram_handle(term))
        return ans

    def except_kgram(self, term1, term2):
        """

        :param term1:
        :param term2:
        :return:
        """
        se1 = self.k_gram_handle(term1)
        se2 = self.k_gram_handle(term2)
        ans = se1.difference(se2)
        return ans
