
from .Cleanable import Cleanable

class Cleaner:

    INSTANCE = None

    def __init__(self):
        self.reset()
        
    def register(self, cleanable_object):
        if isinstance(cleanable_object, Cleanable):
            self._cleanables.append(cleanable_object)
        else:
            print("Attempted to register a non-Cleanable object: " + str(cleanable_object))
            
    def clean(self):
        while len(self._cleanables) > 0:
            self._cleanables.pop().clean()
        
    def reset(self):
        self._cleanables = []
        
    def getCleaner():
        if Cleaner.INSTANCE is None:
            Cleaner.INSTANCE = Cleaner()
        return Cleaner.INSTANCE
           