from multiprocessing import Process

def numbers():
    for i in range(27):
        print(f"{i}")

def letters():
    for j in 'abcdefghijk1mnopqrstuvwxyz':
        print(f"{j}")

pro1 = Process(target=numbers)
pro2 = Process(target=letters)
pro1.start()
pro2.start()
pro1.join()
pro2.join()