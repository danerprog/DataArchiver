from abc import ABC
from abc import abstractmethod

class Cleanable(ABC):

    @abstractmethod
    def clean(self):
        pass