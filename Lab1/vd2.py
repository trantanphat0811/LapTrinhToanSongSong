import numpy as np
numpy_array = np.random.rand(30000, 30000)
x = numpy_array(numpy_array, chunks=(3000, 3000))
result= numpy_array + 1
print(result)