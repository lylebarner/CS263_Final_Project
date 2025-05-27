class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class StreamChecker:
    def __init__(self, words):
        self.root = TrieNode()
        self.stream = []
        self.max_len = max(len(word) for word in words)

        # Build reversed trie
        for word in words:
            node = self.root
            for c in reversed(word):
                if c not in node.children:
                    node.children[c] = TrieNode()
                node = node.children[c]
            node.is_end = True

    def query(self, letter):
        self.stream.append(letter)
        if len(self.stream) > self.max_len:
            self.stream.pop(0)

        node = self.root
        for c in reversed(self.stream):
            if c not in node.children:
                return False
            node = node.children[c]
            if node.is_end:
                return True
        return False
