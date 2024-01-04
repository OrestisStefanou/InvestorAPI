class PredictionDataNotFound(Exception):
    """
    Raised when data to create prediction input are not found
    """
    pass


class InvalidPredictionInput(Exception):
    """
    Raised when the prediction input data are not valid
    """