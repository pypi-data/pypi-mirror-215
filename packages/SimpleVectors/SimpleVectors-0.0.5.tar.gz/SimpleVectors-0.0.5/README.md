# SimpleVectors

Very easy to use module which provides functions to add vectors using their magnitude and direction (angle) w.r.t x-axis. 
All the vectors which will be added are assumed to be passing through the same line



# Usage Example

   
```python
    from  simplevectors  import  simplevector, addvectors
    
    #Create vectors using their magnitude and their angle w.r.t x axis in degrees
    vector1  =  simplevector(10, 0)
    vector2  =  simplevector(10, 90)
    
    resultant_vector  = addvectors(vector1, vector2)
    
    print("Resultant Vector Magnitude: {}, Direction: {}".format(resultant_vector.magnitude, resultant_vector.direction))
```