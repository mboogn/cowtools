
from math import trunc, ceil, floor, modf
from os import urandom, getrandom, GRND_RANDOM
from random import SystemRandom, RECIP_BPF
from sys import byteorder


def tround(n, nd=0):
    if not nd: return trunc(n)
    dx = 10**nd
    return round(trunc(n*dx)/dx, nd)
def ceiround(n, nd=0):
    if not nd: return ceil(n)
    dx = 10**nd
    return round(ceil(n*dx)/dx, nd)
def floround(n, nd=0):
    if not nd: return floor(n)
    dx = 10**nd
    return round(floor(n*dx)/dx, nd)

def zdiround(v, nd=None, zdir=0, rel_zero=True):
    if nd is None: return v
    if rel_zero and v < 0: return (round if not zdir else (tround if zdir < 0 else floround))(v, nd)
    return (round if not zdir else (floround if zdir < 0 else ceiround))(v, nd)


class Syrd(SystemRandom):
    """
    Methods based on random.Random but accessing os.urandom directly.  Most methods have been 
    optimized for speed and/or randomness at unknown (probably negligable) cost.  Randomness can 
    be theoretically increased at a significant (and (seemigly) random; sometimes it’s unnoticeable) 
    cost to speed via Syrd.set_urandom_flags.
    """
    def set_urandom_flags(self, newflags=GRND_RANDOM):
        "Called without input, sets flags to os.GRND_RANDOM, trading randomness quality for speed. "\
        "Called with newflags=0 ( Syrd().set_urandom_flags(0) ), resets to default behavior."
        self.random.__func__.__defaults__ = (newflags,)
        self.randbytes.__func__.__defaults__ = (False, newflags,)
    
    def random(self, *, flags=GRND_RANDOM):
        """Get the next random number in the range [0.0, 1.0)."""
        return (int.from_bytes(getrandom(7, flags=flags), byteorder) >> 3) * RECIP_BPF

    def getrandbits(self, k):
        """getrandbits(k) -> x.  Generates an int with k random bits."""
        if k < 0:
            raise ValueError('number of bits must be non-negative')
        numbytes = (k + 7) // 8                       # bits / 8 and rounded up
        x = int.from_bytes(getrandom(numbytes, flags=GRND_RANDOM), byteorder)
        return x >> (numbytes * 8 - k)                # trim excess bits

    def randbytes(self, n, out_as=None, flags=GRND_RANDOM):
        """Generate n random bytes."""
        # os.urandom(n) fails with ValueError for n < 0
        # and returns an empty bytes string for n == 0.
        if out_as: return out_as(getrandom(n, flags=flags))
        return getrandom(n, flags=flags)
    
    def randrange(self, start, stop=None, step=1, *, nd=0):
        """Choose a random item from range(start, stop[, step]).
        """
        if nd is not None:
            r = self.randrange(start, stop, step, nd=None)
            return nd and floround(r, nd=nd) or int(r)
        rdrd = self.random
        if stop is None:
            if step == 1: return rdrd()*start
            return ((rdrd()*start)//step)*step
        if step == 1: return rdrd()*(stop-start) + start
        return ((rdrd()*(stop-start))//step)*step + start
    
    def randomseq(self, length=1, key=iter):
        if not length: return self.random()
        rf = self.random
        if key: return key((rf() for _ in range(length)))
        return (rf() for _ in range(length))
    
    def randbytseq(self, n, length=1, subkey=None, key=iter):
        rf = self.randbytes
        def rdbtsq(length=length, subke=subkey, key=key):
            if key:
                if subkey: return key((subkey(rf(n)) for _ in range(length)))
                return key((rf(n) for _ in range(length)))
            if subkey: return (subkey(rf(n)) for _ in range(length))
            return (rf(n) for _ in range(length))  
        return rdbtsq
    
    def randrangeseq(self, start, stop=None, step=1, *, length=1, key=iter, nd=None):
        "Returns a function: rdrgsq(length=length, key=key, nd=nd) which returns an iterable of "\
        "type ‘key’ containing random numbers from: \n"\
        "  {n ∈ N | start<=n<⁽¹⁾ stop && n←floor_round(n, nd)⁽¹⁾ && n%floor_round(step, nd) ≈≈ 0} \n"\
        "    ⁽¹⁾†:  If nd is None, n are returned with no rounding. \n"\
        "            If nd==0, n are returned as ints (to accommodate python indexing). \n"\
        "            Otherwise, n are returned floored to the ndᵗʰ digit."   
        rdrd = self.random        
        if stop is None:
            if step == 1:
                rf = lambda: (rdrd()*start)
            else:
                rf = lambda: (((rdrd()*start)//step)*step)
        else:
            span = stop-start
            if step == 1:
                rf = lambda: (rdrd()*(span) + start)
            else:
                rf = lambda: (((rdrd()*(span))//step)*step + start)
        def flrrf(ñ):
            if ñ: return floround(rf(), nd=ñ)
            if ñ is None: return rf()
            return int(rf())
        def rdrgsq(length=length, key=key, nd=nd):
            if key: return key(flrrf(nd) for _ in range(length))
            return (flrrf(nd) for _ in range(length))
        return rdrgsq
    '''
    def get_randbytes_rangeseq(self, start, stop=0, nsteps=256, *, \
    length=1, subkey=int, key=None, nd=0):
        start, stop = not stop and (stop, start) or (start, stop)
        span = stop - start
        nx = 10**nd
        step = int((256 / nsteps)*nx)
        stf = lambda b: round(span * ((b*nx) // step))/nx  + start, nd)
        def rdbtsq(length=length, subke=subkey, key=key):
            if key:
                if subkey: return key((subkey(rf(n)) for _ in range(length)))
                return key((rf(n) for _ in range(length)))
            if subkey: return (subkey(rf(n)) for _ in range(length))
            return (rf(n) for _ in range(length))
        return rdbtsq;'''
         
        


SRNG = Syrd()
SRNG.set_urandom_flags(0)
Srdrd = SRNG.random
Srdrg = SRNG.randrange
Srdbt = SRNG.randbytes
Srdsq = SRNG.randomseq
Srgsq = SRNG.randrangeseq
Srbsq = SRNG.randbytseq

def srd(m, nd=None, unsigned=False, zdir=0, rel_zero=True):
    r = Srdrd() * m
    if unsigned: return r if nd is None else (round if not zdir else (floround if zdir < 0 else ceiround))(r, nd)
    r = r*2 - 1
    return zdiround(r, nd, zdir=zdir, rel_zero=rel_zero)


#improbblsequstr = (lambda *x: lambda*y: (lambda*z: ''.join(chr(int(i)+161) for i in sorted(x+y+z, key=lambda a: Srdrd()))))(*Srdbt(6))(*Srdbt(6))(*Srdbt(6))



__all__ = ['tround', 'ceiround', 'floround', 'zdiround', 'Syrd', 'SRNG', 'Srdrd', 'Srdrg', 'Srdbt', 'Srdsq', 'Srgsq', 'Srbsq', 'srd', 'getrandom'
]

#flo = srd(12, 7)
#floma, floex = frexp(flo)
#florem, floint = modf(flo)

#print(flo, (floma, floex), (florem, floint))
