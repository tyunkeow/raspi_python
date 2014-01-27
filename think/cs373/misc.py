from math import exp, sqrt, pi

# mu = mittel
# sig =varianz
# x = x
def f(mu, sigma2, x):
    covar = sigma2 # pow(sigma, 2)
    return (1 / sqrt(2*covar*pi)) * exp(-0.5 * (x - mu)**2 / covar)

# measurement update - (bayes)
# sigma = s**2
def update(mu1, sigma1, mu2, sigma2):
    mu =  (sigma2 * mu1 + sigma1 * mu2) / (sigma1 + sigma2)
    sigma = 1 / ((1 / sigma1) + (1 / sigma2))
    return [mu, sigma]

#print str(f(10, 4, 10))
# motion update - total prob
def predict(mu1, sigma1, mu2, sigma2):
    mu = mu1 + mu2
    sigma = sigma1 + sigma2
    return mu, sigma

print update(10., 8., 13., 2.)
print predict(8., 4., 10., 6.)

measurements = [5., 6., 7., 9., 10.]
motion = [1., 1., 2., 1., 1.]
measurement_sig = 4.
motion_sig = 2.
mu = 0
sig = 10000

for i in range(len(measurements)):
    mu, sig = update(mu, sig, measurements[i], measurement_sig)
    print "update " + str(mu) + ", " + str(sig)
    mu, sig = predict(mu, sig, motion[i], motion_sig)
    print "predict " + str(mu) + ", " + str(sig)
