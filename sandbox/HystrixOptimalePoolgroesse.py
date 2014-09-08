import math
import scipy.misc
import gmpy

p = 1./84  # Anzahl server
#N = [23.1, 46.2, 28.51, 49.875, 37.38, 49.98, 53.13, 55.75]  # thread
N = [1, 2, 3, 5, 10, 13, 21, 34, 55, 89, 144]  # thread

def binomial(k, p, n):
    return scipy.misc.comb(n, k) * p**k * (1-p)**(n-k)

def binomial_exact(k, p, n):
    return gmpy.comb(n, k) * p**k * (1-p)**(n-k)

# Wahrscheinlichkeit, dass ein Server mehr als k-mal gezogen wurde
def get_prob_X_groesser_k(k, p, n):
    result = 0.
    for i in range(k+1):
        #print "k="+str(k)
        result += binomial(i, p, n)
    return (1. - result)

for n in N:
    #print "------------- n = {} ------------------".format(n)
    print ""
    for poolSize in range(10):
        proz = get_prob_X_groesser_k(poolSize, p, n) * 100
        print "Request Count={0}; Poolsize={1}; Prob Pool exhausted={2:.20g} %".format(n, poolSize, proz)
        #print binomial_exact(k, p, n)


#print binomial(1, 1./100, 100)