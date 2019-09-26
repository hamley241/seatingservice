import numpy as np
import ntpath

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

def validate_positive_int(input):
    pos_int = validate_int(input)
    if pos_int <= 0:
        raise ValueError("Not a positive int {}".format(str(input)))
    return pos_int


def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
