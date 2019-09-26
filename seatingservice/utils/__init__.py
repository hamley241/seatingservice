def memoize(f):
    memo = {}
    print("In memo")
    def helper(x, y):
        if str(y) not in memo:
            print("NOT IN MEMO")
            memo[str(y)] = f(x,y)
        print(memo[str(y)])
        print(str(y))
        return memo[str(y)]
    return helper