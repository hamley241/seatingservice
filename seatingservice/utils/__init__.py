import numpy as np


def memoize(f):
    memo = {}
    print("In memo")

    def helper(x, y):
        if str(y) not in memo:
            print("NOT IN MEMO")
            memo[str(y)] = f(x, y)
        print(memo[str(y)])
        print(str(y))
        return memo[str(y)]

    return helper


def numpy_fillna(data):
    # Get lengths of each row of data
    lens = np.array([len(i) for i in data])

    # Mask of valid places in each row
    mask = np.arange(lens.max()) < lens[:, None]

    # Setup output array and put elements from data into masked positions
    out = np.zeros(mask.shape, dtype=data.dtype)
    out[mask] = np.concatenate(data)
    return out

def validate_int(input):
    try:
        return int(input)
    except Exception as e:
        raise e