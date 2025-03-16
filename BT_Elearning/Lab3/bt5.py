from multiprocessing import Process, current_process

def numbers():
    for i in range(27):
        print(f"{current_process().name}: {i}")

def letters():
    for j in "afasfasfadbndabnadk":
        print(f"{current_process().name}: {j}")

if __name__ == '__main__':
    pro1 = Process(target=numbers, name="Process-Numbers")
    pro2 = Process(target=letters, name="Process-Letters")
    
    pro1.start()
    pro2.start()
    
    pro1.join()
    pro2.join()
