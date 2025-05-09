import threading

def numbers():
    for i in range(27):
        print(f"{i}")

def letters():
    for j in 'abcdefghijk1mnopqrstuvwxyz':
        print(f"{j}")

thread1 = threading.Thread(target=numbers)
thread2 = threading.Thread(target=letters)
thread1.start()
thread2.start()
thread1.join()
thread2.join()