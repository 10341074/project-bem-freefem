from src import *

flag = -999

def Phi1z(z, z0):
  x, y = z.real, z.imag
  x0, y0 = z0.real, z0.imag
  if z == z0:
    return flag
  return 1 / (2 * np.pi) * np.log(1 / np.sqrt((x - x0)**2 + (y - y0)**2))
###########################################################################################################
def e0(tt, st0, st1):
  # first element function
  return (tt - st0) / (st1 - st0)
def e1(tt, st0, st1):
  # second element function
  return (st1 - tt) / (st1 - st0)
def truncate(f):
  return f * (f>=0) * (f<=1)
def truncate_up(f):
  # truncate in the exact quadrature nodes the sum of two element functions
  return 1 + (f - 1) * (f<=1)
def elem_deg1(s, t):
  # compute all element functions for sources s and targets t
  st_ext = np.concatenate( ([s.t[-1] - 1], s.t, [s.t[0] + 1]) )
  A = np.empty((len(t.t), len(s.t)))
  for j in range(1, len(st_ext) - 1 ):
    A[:, j-1] = truncate_up(truncate(e0(t.t, st_ext[j-1], st_ext[j])) + truncate(e1(t.t, st_ext[j], st_ext[j+1])))\
              + truncate_up(truncate(e0(t.t - 1, st_ext[j-1], st_ext[j])) + truncate(e1(t.t - 1, st_ext[j], st_ext[j+1])))\
              + truncate_up(truncate(e0(t.t + 1, st_ext[j-1], st_ext[j])) + truncate(e1(t.t + 1, st_ext[j], st_ext[j+1])))
  return A  
###########################################################################################################

def plot_Phie(ind0, indx, zx = ()):
  if zx != ():
    indx = ind0 + 1 # it's different
  s = sg.Segment(100, f_inargs = (sh.ellipse, (0, 2, 1)), quad='g')
  s_ex = sg.Segment(100, f_inargs = (sh.ellipse, (0, 2, 1)), quad='g')
  A = elem_deg1(s, s_ex)
  if zx == ():
    zx = s.x[indx]
  Phi_ex = np.array([Phi1z(z, zx) for z in s_ex.x])
  vy = list(A[:, ind0] * Phi_ex)
  vx = list(s_ex.t)
  if ind0 == indx:
    indflag = vy.index(flag)
    del vx[indflag]
    del vy[indflag]
  plt.plot(vx, vy, '-+', lw=2)
  plt.show(block=False)
  return Phi_ex[ind0] * s.w[ind0]

def integral():
  tot = 0
  for k in range(99):
    tot = tot + plot_Phie(k, 0, zx = 2)
  print(tot)
  return
def integral2():
  s = sg.Segment(100, f_inargs = (sh.ellipse, (0, 2, 1)), quad='g')
  print(s.x[0])
  K = ly.layerpotS(s=s)
  print(K[0,:].dot(np.ones(99)))
  return


def convergenceIntegralLayerP(n_ex = 100):
  rng = np.arange(10 + (n_ex % 2), n_ex, 10)
  iterInt = np.empty(rng.size, float)
  for nindex, n in enumerate(rng):
    s = sg.Segment(n, f_inargs = (sh.ellipse, (0, 2, 1)), quad='p')
    KS = ly.layerpotS(s = s)
    iterInt[nindex] = KS[0,:].dot(np.ones(n))
    print("point = ", s.x[0])
  return iterInt
def convergenceIntegralLayerG(n_ex = 100):
  rng = np.arange(10 + (n_ex % 2), n_ex, 10)
  iterInt = np.empty(rng.size, float)
  for nindex, n in enumerate(rng):
    s = sg.Segment(n, f_inargs = (sh.ellipse, (0, 2, 1)), quad='gf')
    KS = ly.layerpotS(s = s)
    iterInt[nindex] = KS[0,1:].dot(np.ones(n - 1))
    print("point = ", s.x[0], iterInt[nindex])
  return iterInt
def convergenceIntegralBEM1G(n_ex = 100):
  rng = np.arange(10 + (n_ex % 2), n_ex, 10)
  iterInt = np.empty(rng.size, float)
  for nindex, n in enumerate(rng):
    s = sg.Segment(n, f_inargs = (sh.ellipse, (0, 2, 1)), quad='gf')
    iterInt[nindex] = sum([Phi1z(ix, s.x[0]) * s.w[i] for i, ix in enumerate(s.x)])
    print("point = ", s.x[0], iterInt[nindex])
  return iterInt
def iterPlot(iterv, fig = ()):
  if fig == ():
    fig = plt.figure()
  plt.plot(iterv, '*-', ms=2)
  plt.show(block=False)
  # plt.axis('equal')
  # plt.axis('square')
  return fig
if __name__ == "__main__":
  # plot_Phie(0, 0, zx = 2)
  # integral()
  # integral2()
  n_ex = 300
  iterv = convergenceIntegralLayerP(n_ex)
  fig = iterPlot(iterv)
  ret = input('Press')
  iterv = convergenceIntegralLayerG(n_ex)
  iterPlot(iterv, fig)
  ret = input('Press')
  iterv = convergenceIntegralBEM1G(n_ex)
  iterPlot(iterv, fig)
  ret = input('Press')
