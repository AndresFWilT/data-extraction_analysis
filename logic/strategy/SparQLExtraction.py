from logic.strategy.Extraction import Extraction

class SparQLExtraction(Extraction):
    """
    Concrete strategy that implements the algorithm to extract the data
    from WikiData using SparQL, following the base Strategy Extraction interface
    """
    def do_extraction(self):

        return super().extraction()

    def save_data(self):
        return super().save_data()