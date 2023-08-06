

class simplevector():

    #each vector takes a magnitude and direction in degrees
    def __init__(self, magnitude, direction) -> None:
        self.magnitude = magnitude
        self.direction = direction

class InvalidVectorError(Exception):
    """Exception raised for errors in the input vector.

    Attributes:
        vector -- input vector which caused the error
        message -- explanation of the error
    """

    def __init__(self, vector, message="Please provide simplevector objects and not other variables :("):
        self.vector = vector
        self.message = message
        super().__init__(self.message) 


if __name__ == "__main__":
    a = 10
    b = simplevector(0,0)
    print(isinstance(a, simplevector))
    print(type(b))