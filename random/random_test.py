from math import sqrt as _sqrt
from random import *

## -------------------- test program --------------------

def _test_generator(n, func, args):
    import time
    total = 0.0
    sqsum = 0.0
    smallest = 1e10
    largest = -1e10
    t0 = time.ticks_ms()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x*x
        smallest = min(x, smallest)
        largest = max(x, largest)
    t1 = time.ticks_ms()
    print((t1-t0), 'ms,', end=' ')
    avg = total/n
    stddev = _sqrt(sqsum/n - avg*avg)
    print('avg %g, stddev %g, min %g, max %g' % \
              (avg, stddev, smallest, largest))


def test_lfsr_period(inst):
    inst.setstate(1)
    period=0
    while True:
        inst._shift()
        period+=1
        if inst.getstate() == 1:
            break
    print("Lfsr with polynom 0x%x, size %g bits has a period of %g" %(inst.poly,inst.lfsrsize,period))

def _test(N=2000):
    _test_generator(N, random, ())
    _test_generator(N, randint, (0, 1000))
    _test_generator(N, randrange, (0, 1000))
    _test_generator(N, randrange, (0, 1000,10))
    _test_generator(N, randrange, (0, 1000,2))
    _test_generator(N, randrange, (0, 1000,3))

    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, lognormvariate, (0.0, 1.0))
    _test_generator(N, vonmisesvariate, (0.0, 1.0))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, gauss, (0.0, 1.0))
    _test_generator(N, betavariate, (3.0, 3.0))
    _test_generator(N, triangular, (0.0, 1.0, 1.0/3.0))

    _test_generator(N, getrandbits, {1})
    _test_generator(N, getrandbits, {8})
    _test_generator(N, getrandbits, {32})
    _test_generator(N, getrandbits, {64})
    _test_generator(N, getrandbits, {512})
    
    test_lfsr_period(Random(0x9))
    test_lfsr_period(Random(0x8E))
    test_lfsr_period(Random(0xFA))
    test_lfsr_period(Random(0x204))


    

if __name__ == '__main__':
    _test()
