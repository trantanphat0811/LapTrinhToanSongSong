import threading 
def numbers():
    for i in range (27):
        print (f"{i}")
def letters():
    for j in "vnavnasvnasvnasnva":
        print (f"{j}")

t1 = threading.Thread(target=numbers)
t2= threading.Thread(target=letters)
t1.start()
t2.start()
t1.join()
t2.join()