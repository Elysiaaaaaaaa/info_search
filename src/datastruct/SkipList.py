import random


class _SkipNode:
    """
    表示跳跃表节点的类
    """

    def __init__(self, doc_id, first_idx, level, cnt):
        """
        :param doc_id: 文章索引
        :param first_idx: 第一次出现位置
        :param level: 等级
        :param cnt: term在doc出现次数
        """
        self.doc_id = doc_id
        self.first_idx = first_idx
        self.cnt = cnt
        self.forward = [None] * (level + 1)

    def __len__(self):
        return len(self.forward)

    def __str__(self):
        return '(' + str(self.doc_id) + ', ' + str(self.cnt) +  ', ' + str(self.first_idx) + ')'


class SkipList:
    """
    跳跃表具体实现类
    对应于一个倒排记录
    """

    def __init__(self, max_level=200, portion=0.5):
        """
        创建空的跳跃表
        :param max_level: 跳跃表所有节点引用所可能达到的最高阶数
        :param portion: 具有i-1阶节点引用同时具有i阶引用的比例
        """
        self.MAX_LEVEL = max_level
        self.portion = portion
        self.down_layer = list()
        self.header = self._make_node(self.MAX_LEVEL, None, None, -1)
        self.level = 0  # 跳跃表当前引用阶数
        self.n = 0
        # self.down_layer = []

    def __len__(self):
        """
        返回跳跃表的节点个数
        """
        return self.n

    # def get_next_idx(self,idx):
    #     """
    #     提供类似于链表的查找方式
    #     返回idx+1对应的SkipNode节点
    #     :param idx:
    #     :return:
    #     """
    #     return self.header.forward[0][idx+1]

    def _make_node(self, lvl, doc_id, first_idx, cnt):
        """
        创建新的跳跃表节点
        :param lvl: 新节点所具有的最高引用阶数
        :param doc_id: 文章索引
        :param first_idx: 第一次出现下标
        :param cnt: term在doc出现次数
        :return: 新节点的引用
        """
        node = _SkipNode(doc_id, first_idx, lvl, cnt)
        self.down_layer.append(node)
        return node

    def _random_lvl(self):
        """
        生成新节点的最高引用阶数，不超过预设值
        :return: 新节点的最高引用阶数
        """
        lvl = 0
        while random.random() < self.portion and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def _utility_search(self, doc_id, doc_begin=0):
        """
        查找的实用非公有方法
        :param doc_id: 待查找节点的键
        :return: 元组
        """
        cursor = [None] * (self.MAX_LEVEL + 1)
        current = self.down_layer[doc_begin]
        for i in range(len(current)-1, -1, -1):
            # 当跳跃表为空时，current.forward[0]为None
            while current.forward[i] and current.forward[i].doc_id < doc_id:
                current = current.forward[i]
            cursor[i] = current
        current = current.forward[0]
        return current, cursor

    def skip_search(self, doc_id, doc_begin=0):
        """
        在跳跃表中查找并返回键为doc_id的键值对，当不存在时抛出KeyError异常
        """
        current, _ = self._utility_search(doc_id,doc_begin)
        if current and current.doc_id == doc_id:
            return current
        else:
            return None

    # def line_search(self,idx,doc_id,doc_begin=-1):
    #     """
    #     在跳跃表中线性查找并返回键为doc_id的键值对
    #     """
    #     while idx < doc_id:
    #         idx = self.header.forward[0][idx+1].doc_id
    #         if idx == doc_id:
    #             return self.header.forward[0][idx]
    #     return None

    def skip_insert(self, doc_id, first_begin,cnt):
        """
        向跳跃表中插入由键值对封装后得到的节点
        :param doc_id: 文章索引
        :param first_begin: 第一次出现位置
        """
        current, cursor = self._utility_search(doc_id)
        if current and current.doc_id == doc_id:
            # 重复插入, 更新first_idx和cnt
            current.first_idx = first_begin
            current.cnt = cnt
        else:
            lvl = self._random_lvl()

            if lvl > self.level:
                # 最高阶数刷新
                for i in range(self.level + 1, lvl + 1):
                    cursor[i] = self.header
                self.level = lvl
            # if lvl == self.MAX_LEVEL:
            #     # 存储最高层
            #     self.top_layer.append(doc_id)
            node = self._make_node(lvl, doc_id, first_begin, cnt)
            for i in range(lvl + 1):
                # 更新节点连接状态
                node.forward[i] = cursor[i].forward[i]
                cursor[i].forward[i] = node
            self.n += 1


    def skip_delete(self, doc_id):
        """
        从跳跃表中删除doc_id节点
        """
        current, cursor = self._utility_search(doc_id)
        if current is not None and current.doc_id == doc_id:
            ret = current
            self.down_layer.remove(ret)
            for i in range(self.level + 1):
                if cursor[i].forward[i] != current:
                    break  # 循环从i = 0开始，如从i = self.level开始则使用continue，但不如使用break相对高效
                cursor[i].forward[i] = current.forward[i]
            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            self.n -= 1
            # 更新最高层节点
            # self.top_layer.remove(doc_id)
            return ret

    def term_node_show(self,term):
        """
        展示一个term的全部节点
        :param term:
        :return:
        """
        for i in self.header.forward[0]:
            print(i.doc_id,end=' ')
            print('')


    def skip_display(self):
        print("\n*****Skip List******")
        header = self.header
        for lvl in range(self.level + 1):
            print("Level {}: ".format(lvl), end=" ")
            node = header.forward[lvl]
            while node is not None:
                print(node.doc_id, end=" ")
                node = node.forward[lvl]
            print('')
        for i in self.down_layer:
            print(i.doc_id,end=' ')


if __name__ == '__main__':
    skip_list = SkipList(10, 0.5)
    skip_list.skip_insert(3, 5, 3)
    skip_list.skip_insert(12, 9, 3)
    skip_list.skip_insert(12, 9, 4)
    skip_list.skip_insert(12, 9, 6)
    skip_list.skip_insert(12, 1, 8)
    skip_list.skip_insert(26, 7, 1)
    skip_list.skip_insert(7, 13, 9)
    skip_list.skip_insert(21, 3, 8)
    skip_list.skip_insert(25, 4, 1)
    skip_list.skip_insert(6, 6, 5)
    skip_list.skip_insert(17, 8, 2)
    skip_list.skip_insert(19, 10, 1)
    skip_list.skip_insert(9, 14, 399)
    print(len(skip_list))  # 10
    print(skip_list.skip_search(3))  # (3, 5)
    print(skip_list.skip_delete(19))  # (19, 10)
    print(skip_list.skip_delete(12))  # (19, 10)
    print(skip_list.skip_delete(3))  # (19, 10)
    print(len(skip_list))  # 9
    skip_list.skip_display()
