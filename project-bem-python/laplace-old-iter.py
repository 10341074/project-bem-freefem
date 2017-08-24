from src import *
import numpy.random

def g1(z):
  x, y = z.real, z.imag
  return exp(x) - 4 * cos(2*y)
def g2(z):
  x, y = z.real, z.imag
  return exp(x) + cos(2*y)
def E(z, z0):
  x, y = z.real, z.imag
  x0, y0 = z0.real, z0.imag
  return 1 / (2 * np.pi) * np.log(1 / np.sqrt((x - x0)**2 + (y - y0)**2))


def randSelectUnif(s, intx, inty = (), n = 100000):
  if inty == ():
    inty = intx
  ax, bx, ay, by = *intx, *inty
  sample = np.empty(n, complex)
  for k in range(n):
    z = complex(numpy.random.uniform(ax, bx) + 1j *  numpy.random.uniform(ay, by))
    while s.contains(z) == 0:
      z = complex(numpy.random.uniform(ax, bx) + 1j *  numpy.random.uniform(ay, by))
    sample[k] = z
  return sample

def integral(sample, z0):
  samplecopy = np.array(list(filter(lambda a: a != z0 , sample)))
  print(len(samplecopy), " < ", len(sample))
  e = E(samplecopy, z0)
  return sum(e) / len(samplecopy)


if __name__ == "__main__":
  s = gm.sg_one_ellipse(10)
  arr = np.arange(1,10) * 1e4
  v = np.empty(9, float)
  for k in range(len(arr)):
    sample = np.array(randSelectUnif(s, (-5, 5), n = int(arr[k])))
    v[k] = integral(sample, sample[56])
  plt.plot(v, '+-')
  # plt.plot(sample.real, sample.imag, '*')
  plt.show(block=False)
  # print(integral(sample, sample[56]))
  ret = input('Press')
  
