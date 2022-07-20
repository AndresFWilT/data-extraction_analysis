from __future__ import annotations
from abc import ABC
from logic.strategy.Extraction import Extraction



class Data():
    """
    The context that defines the interface of interest to user
    """

    def __init__(self,extraction: Extraction) -> None:
        """
        Strategy trough context (extraction, data)
        """
        self._extraction = extraction

    @property
    def extraction(self) -> Extraction:
        """
        The context maintains a reference to one of the Strategy objects.
        """
        return self._extraction
    
    @extraction.setter
    def extraction(self, extraction: Extraction) -> None:
        """
        setter for replacing a Extraction object at runtime
        """
        self._extraction = extraction

    def execute_extraction(self) -> None:
        """
        The context delegates some work to the Strategy (Extraction) object instead
        of implementing multiple versions of the algorithm on its own
        """
        print("Executing data extraction..")
        self._extraction.do_extraction()
        print("Saving data..")
        self._extraction.save_data()
    
    def get_extraction(self) -> None:
        """
        The context delegates some work to the Strategy (Extraction) object instead
        of implementing multiple versions of the algorithm on its own
        """
        print("Getting data extracted")
        return self._extraction.get_data()