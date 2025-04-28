class BPlusTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.next = None  # tylko dla liści


class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusTreeNode(True)
        self.order = order
        self.nick_to_score = {}  # odwzorowanie nick -> score
        self.comparisons = 0

    def _find_leaf(self, score):
        self.comparisons = 0
        node = self.root
        while not node.leaf:
            i = 0
            while i < len(node.keys):
                self.comparisons += 1
                if score < node.keys[i]:
                    break
                i += 1
            node = node.children[i]
        return node

    def add_player(self, nick, score):
        if nick in self.nick_to_score:
            raise ValueError(f"Gracz {nick} już istnieje.")
        self.nick_to_score[nick] = score
        node = self._find_leaf(score)
        i = 0
        while i < len(node.keys) and score > node.keys[i]:
            self.comparisons += 1
            i += 1
        if i < len(node.keys) and node.keys[i] == score:
            node.children[i].append(nick)
        else:
            node.keys.insert(i, score)
            node.children.insert(i, [nick])
            if len(node.keys) >= self.order:
                self._split_leaf(node)

    def _split_leaf(self, node):
        new_node = BPlusTreeNode(True)
        mid = len(node.keys) // 2
        new_node.keys = node.keys[mid:]
        new_node.children = node.children[mid:]
        node.keys = node.keys[:mid]
        node.children = node.children[:mid]

        new_node.next = node.next
        node.next = new_node

        if node == self.root:
            new_root = BPlusTreeNode(False)
            new_root.keys = [new_node.keys[0]]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            self._insert_in_parent(node, new_node.keys[0], new_node)

    def _insert_in_parent(self, node, key, new_node):
        parent = self._find_parent(self.root, node)
        i = parent.children.index(node)
        parent.keys.insert(i, key)
        parent.children.insert(i + 1, new_node)
        if len(parent.keys) >= self.order:
            self._split_internal(parent)

    def _split_internal(self, node):
        new_node = BPlusTreeNode(False)
        mid = len(node.keys) // 2
        mid_key = node.keys[mid]

        new_node.keys = node.keys[mid + 1:]
        new_node.children = node.children[mid + 1:]

        node.keys = node.keys[:mid]
        node.children = node.children[:mid + 1]

        if node == self.root:
            new_root = BPlusTreeNode(False)
            new_root.keys = [mid_key]
            new_root.children = [node, new_node]
            self.root = new_root
        else:
            self._insert_in_parent(node, mid_key, new_node)

    def _find_parent(self, current, child):
        if current.leaf or current.children[0].leaf:
            return None
        for i in range(len(current.children)):
            if current.children[i] == child:
                return current
            res = self._find_parent(current.children[i], child)
            if res:
                return res
        return None

    def get_players_in_range(self, low, high):
        result = []
        node = self._find_leaf(low)
        while node:
            for i, score in enumerate(node.keys):
                self.comparisons += 1
                if low <= score <= high:
                    result.extend(node.children[i])
                elif score > high:
                    return result
            node = node.next
        return result

    def get_best_player(self):
        node = self.root
        while not node.leaf:
            node = node.children[-1]
        if not node.keys:
            return None
        max_score = node.keys[-1]
        return node.children[-1][0], max_score

    def get_worst_player(self):
        node = self.root
        while not node.leaf:
            node = node.children[0]
        if not node.keys:
            return None
        min_score = node.keys[0]
        return node.children[0][0], min_score

    def get_score(self, nick):
        score = self.nick_to_score.get(nick)
        self.comparisons = 1
        return score

    def update_score(self, nick, new_score):
        if nick not in self.nick_to_score:
            raise ValueError("Gracz nie istnieje.")
        old_score = self.nick_to_score[nick]
        self.remove_player(nick)
        self.add_player(nick, new_score)

    def remove_player(self, nick):
        if nick not in self.nick_to_score:
            raise ValueError("Gracz nie istnieje.")
        score = self.nick_to_score[nick]
        node = self._find_leaf(score)
        for i in range(len(node.keys)):
            self.comparisons += 1
            if node.keys[i] == score:
                if nick in node.children[i]:
                    node.children[i].remove(nick)
                    if not node.children[i]:
                        del node.children[i]
                        del node.keys[i]
                    break
        del self.nick_to_score[nick]


tree = BPlusTree(order=4)

tree.add_player("Ala", 1200)
tree.add_player("Robert", 1500)
tree.add_player("Karol", 1300)
tree.add_player("Dawid", 1500)

print(tree.get_players_in_range(1200, 1500))  
print(tree.get_best_player())                
print(tree.get_worst_player())             

tree.update_score("Karol", 1600)
print(tree.get_score("Karol"))           

tree.remove_player("Ala")
print(tree.get_players_in_range(1000, 1600))
