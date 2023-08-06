from abc import ABC, abstractmethod

class IReporter(ABC):

    @abstractmethod
    def report():
        pass

    @abstractmethod
    def set_successor():
        pass
    @abstractmethod
    def set_data():
        pass
class IMethod(ABC):

    @abstractmethod
    def evaluate():
        pass

    @abstractmethod
    def set_succesor():
        pass