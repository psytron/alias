


def block( in_something , block_size=16 ):
    in_str = str( in_something )
    lendiff = block_size - len( in_str )
    pre_trunc = in_str+' '* lendiff
    return pre_trunc[:block_size]

def blockprint(s,b=16):
    return s+' '*(b-len(str(s)))

def block_right( in_something , block_size=10):
    return str( in_something[-block_size:] ).rjust(block_size)


def ptest():
    print(' P-TEST Is RunnIng finE ')