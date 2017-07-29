from multiprocessing import Value


class Counter(object):
    def __init__(self, default=50):
        self.val = Value('i', default)

    def increment(self, n=1):
        with self.val.get_lock():
            self.val.value += n

    def set(self, newValue):
    	with self.val.get_lock():
    		self.val.value = newValue

    @property
    def value(self):
        return self.val.value

speed = Counter()
brightness = Counter()
