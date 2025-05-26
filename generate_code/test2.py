class Solution(object):
    def lexicographicallySmallestString(self, s):
        """
        :type s: str
        :rtype: str
        """
        from collections import deque

        visited = set()
        result = s
        queue = deque()
        queue.append(s)
        visited.add(s)

        def is_consecutive(a, b):
            diff = abs(ord(a) - ord(b))
            return diff == 1 or diff == 25  # handle circular 'a'-'z'

        while queue:
            curr = queue.popleft()
            result = min(result, curr)

            for i in range(len(curr) - 1):
                if is_consecutive(curr[i], curr[i+1]):
                    # Remove the pair and form new string
                    new_str = curr[:i] + curr[i+2:]
                    if new_str not in visited:
                        visited.add(new_str)
                        queue.append(new_str)

        return result
