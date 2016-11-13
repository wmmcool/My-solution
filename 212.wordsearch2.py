# Solution leetcode-212 word_search 2

class Solution(object):
    def findWords(self, board, words):
        root = {}
        for word in words:
            current = root
            for letter in word:
                current = current.setdefault(letter, {})
            current['#'] = '#'
        res = []
        
        for i in range (len(board)):
            for j in range (len(board[0])):
                self.find(i, j, board, root, res, '')
        return list(set(res))
        
    def find(self, i, j, board, root, res, path):
        if '#' in root:
            res.append(path)
        if i<0 or i >= len(board) or j<0 or j>=len(board[0]) or board[i][j] not in root:
            return 
        temp = board[i][j]
        board[i][j] = '.'
        self.find(i+1, j, board, root[temp], res, path+temp)
        self.find(i-1, j, board, root[temp], res, path+temp)
        self.find(i, j+1, board, root[temp], res, path+temp)
        self.find(i, j-1, board, root[temp], res, path+temp)
        board[i][j] = temp
        
        """
        :type board: List[List[str]]
        :type words: List[str]
        :rtype: List[str]
        """
        
