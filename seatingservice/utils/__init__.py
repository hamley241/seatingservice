def memoize(f):
    memo = {}
    print("In memo")
    def helper(x):
        if x not in memo:
            memo[x] = f(x)
        return memo[x]
    return helper