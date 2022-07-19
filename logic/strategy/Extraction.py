from abc import ABC,abstractmethod

class Extraction(ABC):
    """
    Interface that declares the opreationes to all supported versions
    of the extraction algorithm

    The context (Data), use this interface to call the alforithm defined by
    Concrete strategies.
    """

    @abstractmethod
    def do_extraction(self):
        pass

    @abstractmethod
    def save_data(self):
        pass