from algorithms.queues.queue import ArrayQueue

class ArrayQueueM(ArrayQueue):

    def __init__(self):
        super().__init__()
        self._array = None

    @property
    def array(self):
        return self._array[self._front]
    
    @array.setter
    def array(self, value):
        self._array = [None] * value

    def enqueue(self, value):
            if self._rear == len(self._array):
                self._expand()
            self._array[self._rear] = value
            self._rear += 1
            self._size += 1

    def get_prox_value(self):
        return self._array[self._rear]

    def is_full(self):
        return self._rear == len(self._array)
    



