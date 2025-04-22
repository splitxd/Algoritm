import unittest

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.height = 1
        self.left = None
        self.right = None


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def update_height(self, node):
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

    def get_balance(self, node):
        return self.get_height(node.left) - self.get_height(node.right) if node else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)
        return y

    def balance(self, node):
        self.update_height(node)
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) < 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) > 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        if key < node.key:
            node.left = self._insert(node.left, key)
        elif key > node.key:
            node.right = self._insert(node.right, key)
        else:
            return node

        return self.balance(node)

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _min_value_node(self, node):
        while node.left:
            node = node.left
        return node

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            temp = self._min_value_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        return self.balance(node)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def search(self, key):
        return self._search(self.root, key) is not None

    def inorder_traversal(self):
        res = []

        def _inorder(node):
            if node:
                _inorder(node.left)
                res.append(node.key)
                _inorder(node.right)

        _inorder(self.root)
        return res

    def find_next(self, key):
        succ = None
        node = self.root
        while node:
            if key < node.key:
                succ = node
                node = node.left
            else:
                node = node.right
        return succ.key if succ else None

    def find_prev(self, key):
        pred = None
        node = self.root
        while node:
            if key > node.key:
                pred = node
                node = node.right
            else:
                node = node.left
        return pred.key if pred else None



class TestAVLTree(unittest.TestCase):
    def test_operations(self):
        tree = AVLTree()
        values = [20, 4, 15, 70, 50, 100, 3]
        for v in values:
            tree.insert(v)

        self.assertTrue(tree.search(15))
        self.assertFalse(tree.search(99))
        tree.delete(15)
        self.assertFalse(tree.search(15))

        expected = sorted([v for v in values if v != 15])
        self.assertEqual(tree.inorder_traversal(), expected)

        self.assertEqual(tree.find_next(20), 50)
        self.assertEqual(tree.find_prev(20), 4)

        tree.insert(15)
        self.assertTrue(tree.search(15))


if __name__ == '__main__':
    unittest.main()