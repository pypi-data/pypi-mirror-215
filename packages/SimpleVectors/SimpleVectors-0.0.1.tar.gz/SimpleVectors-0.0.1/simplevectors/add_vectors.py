import math
import numpy as np
from SimpleVector import simplevector, InvalidVectorError





#add accepts multiple vectors as simplevector objects and returns a resultant vector as a simplevector object. 
def add(*args):
    resultant_vector = simplevector(0,0)
    unit_vectors = []
    magnitude_vectors = []
    force_vectors = []

    for vector in args:
        #
        if isinstance(vector, simplevector) == False:
            raise InvalidVectorError(vector=vector)
        
        direc = math.radians(vector.direction)
        unit_vectors.append([math.cos(direc), math.sin(direc)])
        magnitude_vectors.append([vector.magnitude])
        force_vectors.append([vector.magnitude*math.cos(direc),vector.magnitude*math.sin(direc)])

    unit_vectors = np.array(unit_vectors)
    magnitude_vectors = np.array(magnitude_vectors)



    res = np.dot(unit_vectors.T,magnitude_vectors)
    force_vectors = np.array(force_vectors)

    resdirec = math.atan(res[1][0]/res[0][0])
    resmag = res[0][0]/math.cos(resdirec)
    resultant_vector.magnitude = resmag
    resultant_vector.direction = math.degrees(resdirec)

    return resultant_vector

