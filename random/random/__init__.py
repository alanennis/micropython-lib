# Simple lfsr based implemenration of the module random.
# The default lfsr is 30bits long to keep it fast, a bigger polynomial can be used. 

__all__ = ["Random","seed","random","uniform","randint","choice","sample",
           "randrange","shuffle","normalvariate","lognormvariate",
           "expovariate","vonmisesvariate","gammavariate","triangular",
           "gauss","betavariate","paretovariate","weibullvariate",
           "getstate","setstate", "getrandbits"]

from math import  log as _log

class Random():

    def __init__(self, polynomial = 0x20000029):
        self.state = 1
        self.lfsrsize = int(_log(polynomial,2))+1
        self.lsb = 2**-self.lfsrsize
        self.poly = polynomial
        self.gauss_next = None 
    def _shift(self):
        if self.state & 1 != 0:
            self.state>>=1
            self.state^=self.poly
        else:
            self.state>>=1
       
    def getstate(self):
        return self.state

    def setstate(self, state):
        self.state=state

    def random(self):
        self._shift()
        return (self.state-1) *  self.lsb

    def getrandbits(self, k):
        numpass = (k + self.lfsrsize-1) // self.lfsrsize
        x = 0
        for i in range(0,numpass):
            x<<=self.lfsrsize
            self._shift()
            x+=self.state 
        return x >> (numpass * self.lfsrsize - k)

    def seed(self, *args, **kwds):
        self.setstate(args[0])
        return None

## ---- Methods below this point do not need to be overridden when
## ---- subclassing for the purpose of using a different core generator.

## -------------------- pickle support  -------------------

    def __getstate__(self): # for pickle
        return self.getstate()

    def __setstate__(self, state):  # for pickle
        self.setstate(state)

    def __reduce__(self):
        return self.__class__, (), self.getstate()

## -------------------- integer methods  -------------------

    def randrange(self, start, stop=None, step=1, int=int):
        import random.integers
        return integers.randrange(self,start,stop,step,int)

    def randint(self, a, b):
        return int(a+(b+1-a)*self.random())

## -------------------- sequence methods  -------------------

    def choice(self, seq):
        import sequences
        return sequences.choice(self, seq)

    def shuffle(self, x, random=None, int=int):
        import sequences
        return sequences.shuffle(self, x, random, int)

    def sample(self, population, k):
        import sequences
        return sequences.sample(self, population, k)
## -------------------- real-valued distributions  -------------------

## -------------------- uniform distribution -------------------

    def uniform(self, a, b):
        "Get a random number in the range [a, b) or [a, b] depending on rounding."
        return a + (b-a) * self.random()

## -------------------- triangular --------------------

    def triangular(self, low=0.0, high=1.0, mode=None):
        import random.floats
        return random.floats.triangular(self, low, high, mode)

## -------------------- normal distribution --------------------

    def normalvariate(self, mu, sigma):
        import random.floats
        return random.floats.normalvariate(self, mu, sigma)

## -------------------- lognormal distribution --------------------

    def lognormvariate(self, mu, sigma):
        import random.floats
        return random.floats.lognormvariate(self, mu, sigma)

## -------------------- exponential distribution --------------------

    def expovariate(self, lambd):
        import random.floats
        return random.floats.expovariate(self, lambd)

## -------------------- von Mises distribution --------------------

    def vonmisesvariate(self, mu, kappa):
        import random.floats
        return random.floats.vonmisesvariate(self, mu, kappa)

## -------------------- gamma distribution --------------------

    def gammavariate(self, alpha, beta):
        import random.floats
        return random.floats.gammavariate(self, alpha, beta)

## -------------------- Gauss (faster alternative) --------------------

    def gauss(self, mu, sigma):
        import random.floats
        return random.floats.gauss(self, mu, sigma)

## -------------------- beta --------------------
## See
## http://sourceforge.net/bugs/?func=detailbug&bug_id=130030&group_id=5470
## for Ivan Frohne's insightful analysis of why the original implementation:
##
##    def betavariate(self, alpha, beta):
##        # Discrete Event Simulation in C, pp 87-88.
##
##        y = self.expovariate(alpha)
##        z = self.expovariate(1.0/beta)
##        return z/(y+z)
##
## was dead wrong, and how it probably got that way.

    def betavariate(self, alpha, beta):
        import random.floats
        return random.floats.betavariate(self, alpha, beta)

## -------------------- Pareto --------------------

    def paretovariate(self, alpha):
        import random.floats
        return random.floats.paretovariate(self, alpha)

## -------------------- Weibull --------------------

    def weibullvariate(self, alpha, beta):
        import random.floats
        return random.floats.weibullvariate(self, alpha, beta)

# Create one instance, seeded from current time, and export its methods
# as module-level functions.  The functions share state across all uses
#(both in the user's code and in the Python libraries), but that's fine
# for most programs and is easier for the casual user than making them
# instantiate their own Random() instance.

_inst = Random()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits

