from abc import ABC, abstractmethod

class Adapter[S, T](ABC):
    @abstractmethod
    def adapt(self, source: S) -> T: ...