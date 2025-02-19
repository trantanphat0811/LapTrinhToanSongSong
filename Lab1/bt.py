import time
def inc(x):
    time.sleep(1)
    return x+1

from tqdm import tqdm
ls= []
for i in tqdm(range(60)):
    ls.append(inc(i))
ls[:5]
print(ls[:5])