def choice(self, seq):
    """Choose a random element from a non-empty sequence."""
    try:
        i = self.rangrange(0,len(seq))
    except ValueError:
        raise IndexError('Cannot choose from an empty sequence')
    return seq[i]

def shuffle(self, x, random=None, int=int):
    """x, random=random.random -> shuffle list x in place; return None.

    Optional arg random is a 0-argument function returning a random
    float in [0.0, 1.0); by default, the standard random.random.
    """

    randbelow = self.randrange(0,len(x))
    for i in reversed(range(1, len(x))):
        # pick an element in x[:i+1] with which to exchange x[i]
        j = randbelow(i+1) if random is None else int(random() * (i+1))
        x[i], x[j] = x[j], x[i]

def sample(self, population, k):
    """Chooses k unique random elements from a population sequence or set.

    Returns a new list containing elements from the population while
    leaving the original population unchanged.  The resulting list is
    in selection order so that all sub-slices will also be valid random
    samples.  This allows raffle winners (the sample) to be partitioned
    into grand prize and second place winners (the subslices).

    Members of the population need not be hashable or unique.  If the
    population contains repeats, then each occurrence is a possible
    selection in the sample.

    To choose a sample in a range of integers, use range as an argument.
    This is especially fast and space efficient for sampling from a
    large population:   sample(range(10000000), 60)
    """

    # Sampling without replacement entails tracking either potential
    # selections (the pool) in a list or previous selections in a set.

    # When the number of selections is small compared to the
    # population, then tracking selections is efficient, requiring
    # only a small set and an occasional reselection.  For
    # a larger number of selections, the pool tracking method is
    # preferred since the list takes less space than the
    # set and it doesn't suffer from frequent reselections.

    if isinstance(population, _collections.Set):
        population = tuple(population)
    if not isinstance(population, _collections.Sequence):
        raise TypeError("Population must be a sequence or Set.  For dicts, use list(d).")
    n = len(population)
    if not 0 <= k <= n:
        raise ValueError("Sample larger than population")
    result = [None] * k
    setsize = 21        # size of a small set minus size of an empty list
    if k > 5:
        setsize += 4 ** _ceil(_log(k * 3, 4)) # table size for big sets
    if n <= setsize:
        # An n-length list is smaller than a k-length set
        pool = list(population)
        for i in range(k):         # invariant:  non-selected at [0,n-i)
            j = randint(0,n-i-1)
            result[i] = pool[j]
            pool[j] = pool[n-i-1]   # move non-selected item into vacancy
    else:
        selected = set()
        selected_add = selected.add
        for i in range(k):
            j = randbelow(n)
            while j in selected:
                j = self.randint(0,n-1)
            selected_add(j)
            result[i] = population[j]
    return result

