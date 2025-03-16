from multiprocessing import Pool

def mu(n, p):
    return n ** p

if __name__ == '__main__':
    with Pool(5) as p:
        result = p.starmap(mu, [(4, 3), (5, 3), (6, 3), (7, 3)])
        print(result)
