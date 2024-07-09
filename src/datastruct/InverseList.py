class _InverseNode:
    """
    对应于一个倒排记录
    表示文章节点的类
    """
    def __init__(self, doc_id, term_idx, tf):
        """
        :param doc_id: 文章索引
        :param term_idx: 出现位置信息
        :param level: 等级
        :param tf: term在doc出现次数
        """
        self.doc_id = doc_id
        self.term_idx = term_idx
        self.tf = tf


class InverseList:
    """
    倒排表表具体实现类
    """

    def __init__(self,term):
        """
        创建空的倒排表
        """
        # 元素为_InverseNode
        # self.term = term
        self.nodes = []
        self.term = term

    def __len__(self):
        """
        返回跳跃表的节点个数
        """
        return len(self.nodes)

    def df(self):
        return len(self.nodes)

    def to_set(self):
        ans = set()
        for node in self.nodes:
            ans.add(node.doc_id)
        return ans

    def search(self, doc_id, doc_begin=0):
        """
        在跳跃表中查找并返回键为doc_id的键值对
        """
        for i in range(doc_begin,len(self.nodes)):
            if self.nodes[i].doc_id == doc_id:
                return i
        return -1

    def insert(self, doc_id, term_idx, tf):
        """
        向表中插入由键值对封装后得到的节点
        :param doc_id: 文章索引
        :param term_idx: 出现位置
        :param tf: term在doc出现次数
        """
        node = _InverseNode(doc_id, term_idx, tf)
        self.nodes.append(node)

    def delete(self, doc_id:int,begin_idx=0):
        """
        从表中删除doc_id节点
        """
        idx = self.search(doc_id, begin_idx)
        if idx != -1:
            del self.nodes[idx]

    def exchange(self, doc_id:int, term_idx, tf, begin_idx=0):
        """
        从表中修改doc_id节点
        """
        idx = self.search(doc_id, begin_idx)
        if idx != -1:
            self.nodes[idx] = _InverseNode(doc_id, term_idx, tf)
