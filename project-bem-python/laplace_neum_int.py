from src import *

def g(z):
  x, y = z.real, z.imag
  return 0.5 * (x**3 - 3 * x * y**2)

s = gm.sg_one_ellipse(50)

MS = ly.layerpotSD(s=s)
M = MS + 0.5 * np.eye(s.n)

a00 = sum(s.w * s.x.real**2)
a01 = (s.w * s.x.real**2).dot(MS)
a10 = np.zeros((s.n,1))

rhs = np.concatenate(( [-2], g(s.x) ))
row0 = np.concatenate(( np.array([[a00]]), np.array([a01]).T )).T
row1 = np.concatenate(( a10.T, M.T )).T
A = np.concatenate([row0, row1])

psi = linalg.solve(A, rhs)
print(psi)

p = m.EIT()
p.domain()
p.meshgrid((-2, 2, 100))
p.z = ly.layerpotS(s=s, t=p.pp).dot(psi[1:]) + psi[0] - g(p.pp.x)
p.plot()
p.z = g(p.pp.x)
p.plot()
ret = input('Press')
