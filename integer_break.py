class Solution(object):
    def __init__(self):
        self.memoize = {}
    
    def integerBreak(self, n):
        """Top down approach"""
        # base case: n = 1 + 1, 1*1 = 1
        if n <= 2:
            return 1
        
        if n in self.memoize:
            return self.memoize[n]
        
        ans = 1 * (n-1)
        for i in range(2, n):
            firstNum = i
            secondNum = n - i
            product = firstNum * max(secondNum, self.integerBreak(secondNum))
            if product > ans:
                ans = product
        
        self.memoize[n] = ans
        
        return ans


    def integerBreak2(self, n):
        """Mathematical method"""
        if n <= 2:
            return 1
        if n == 3:
            return 2
        
        numThrees = n // 3
        numTwos = 0
        
        # if remainder division returns 1
        # reduce amount of 3s by one
        # increase amount of 2s by one
        if n % 3 == 1:
            numThrees -= 1
            numTwos = 2
        elif n % 3 == 2:
            numTwos = 1
        
        return (2**numTwos)*(3**numThrees)
    
        
    def integerBreak3(self, n):
        """Bottom-up approach"""
        dp = [0] * (n+1)
        dp[1] = 1
        
        for i in range(2, n+1):
            for j in range(1, i):
                dp[i] = max(dp[i], max[j, dp[j]]) * max(i-j, dp[i-j])
        
        return dp[n]
        
        
sol = Solution()
ans = sol.integerBreak(n=5)
print(ans)