import mc3.stats as ms

loc = 3.0
lo = 0.5
up = 0.75
ppf = ms.ppf_gaussian(loc, lo, up)
pmin = 0.0
pmax = 4.0
tppf = ms.ppf_gaussian(loc, lo, up, pmin, pmax)

u = np.logspace(-10, np.log10(0.5), 50)
u = np.concatenate((u[:-1], 1-u[::-1]))

t1 = time.time()
p1 = ppf(u)
t2 = time.time()
print(f'PPF1: {t2-t1:.4f}')
t1 = time.time()
p2 = tppf(u)
t2 = time.time()
print(f'PPF2: {t2-t1:.4f}')

plt.figure(1)
plt.clf()
ax = plt.subplot(211)
plt.plot(p2, u, '.-', c='b', lw=1.0)
plt.plot(p1, u, '.-', c='orange', lw=1.0, alpha=0.6)
plt.ylim(0, 1)
plt.xlim(pmin-1, pmax+2)
plt.axvline(loc, color='xkcd:green', zorder=-1)
plt.axvline(pmin, color='r')
plt.axvline(pmax, color='r')

size = 100000
r1 = ppf.rv_lo.rvs(size=int(size/0.91))
r2 = tppf.rv_lo.rvs(size=size)
r3 = tppf(np.random.uniform(size=size))

ax = plt.subplot(212)
plt.hist(r1, bins=40, range=(-1,7), color='darkorange', alpha=0.4)
plt.hist(r2, bins=40, range=(-1,7), color='blue', alpha=0.4)
plt.hist(r3, bins=40, range=(-1,7), color='xkcd:green', alpha=0.4)
plt.axvline(loc, color='xkcd:green', zorder=-1)
plt.axvline(pmin, color='r')
plt.axvline(pmax, color='r')
plt.xlim(pmin-1, pmax+2)

