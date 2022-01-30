import time
class Timer:

    def __enter__(self):
        self.t0 = time.time()

    def __exit__(self, *args):
        t1 = time.time()
        print('Elapsed time: %.3f s' % (t1 - self.t0))

