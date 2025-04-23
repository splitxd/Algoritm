import time
import random
import string

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.value = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        node = self.root
        for char in word:

            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.value = word

    def get(self,word:str):
        node = self._search(word)
        if node and node.is_end_of_word:
            return node.value
        return "NOT FOUND"

    def search(self, key: str):
        node = self._search(key)
        return node is not None and node.is_end_of_word

    def _search(self, word: str):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node

    def search_prefix(self, prefix: str):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

    def delete(self, word: str):
        self._delete(self.root, word, 0)

    def _delete(self, node, word, index):
        if index == len(word):
            if not node.is_end_of_word:
                return False
            node.is_end_of_word = False
            node.value = None
            return len(node.children) == 0
        char = word[index]
        next_node = node.children.get(char)
        if next_node is None:
            return False
        should_delete_node = self._delete(next_node, word, index + 1)

        if should_delete_node:
            del node.children[char]
            return len(node.children) == 0 and not node.is_end_of_word

        return False

    def startswith(self, prefix):
        words = []
        node = self.root

        for c in prefix:
            if c not in node.children:
                return words
            node = node.children[c]

        def _dfs(node, path):
            if node.is_end_of_word:
                words.append("".join(path))

            for char, child_node in node.children.items():
                _dfs(child_node, path + [char])

        _dfs(node, list(prefix))
        return words

    def list_words(self):
        words = []
        def _dfs(node, path):
            if node.is_end_of_word:
                words.append("".join(path))

            for char, child_node in node.children.items():
                _dfs(child_node, path + [char])
        _dfs(self.root, [])

        return words

def random_word(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

if __name__ == "__main__":
    trie_dict = Trie()
    num_items = 100_000
    words = [random_word() for _ in range(num_items)]

    print("Вставка")
    start = time.time()
    for i, word in enumerate(words):
        trie_dict.insert(word)
    print(time.time() - start)

    print("Поиск")
    start = time.time()
    found = sum(1 for word in words if trie_dict.search(word))
    print(time.time() - start)





