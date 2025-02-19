import numpy as np
import dask.array as da
import time

numpy_array = np.random.rand(30000, 30000)
x = da.from_array(numpy_array, chunks=(3000, 3000))
start = time.time()
result = x + 1
result.compute()
end = time.time()
print(f"Thời gian thực thi: {end - start:.2f} giây")
