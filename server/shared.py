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

tickrate = Counter()
ticksize = Counter()
brightness = Counter()
generic1 = Counter()
generic2 = Counter()
generic3 = Counter()

alarm_duration = Counter()

alarm_duration.set(10)
ticksize.set(1)
generic3.set(500)
