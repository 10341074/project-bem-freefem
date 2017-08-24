from src import *
import numpy.random

def randSelectUnif(s, intx, inty = (), n = 1000):
  if inty == ():
    inty = intx
  ax, bx, ay, by = *intx, *inty
  sampleUnif = list(map(list, zip(numpy.random.uniform(ax, bx, n), numpy.random.uniform(ay, by, n))))
  sample = np.array(sampleUnif)
  plt.plot(sample[:,0], sample[:,1], '*r')
  plt.show(block=False)
  plt.figure()
  print(len(sampleUnif))
  for it in sampleUnif:
    ret = s.contains(complex(it[0] + 1j * it[1]))
    if ret == 0:
      print(it)
      del(it)
      # sampleUnif.pop(sampleUnif.index(it))
  print(len(sampleUnif))
  return sampleUnif
if __name__ == "__main__":
  s = gm.sg_one_ellipse(10)
  sample = np.array(randSelectUnif(s, (-5, 5)))
  plt.plot(sample[:,0], sample[:,1], '*')
  plt.show(block=False)
  ret = input('Press')
  
