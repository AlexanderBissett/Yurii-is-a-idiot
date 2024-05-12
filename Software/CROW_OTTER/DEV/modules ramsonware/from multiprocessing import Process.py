from multiprocessing import Process
import threading

def loopa():
    threading.Timer(0.1, loopa).start()
    print("aaaaaaaaaaaaaa")
    

def loopb():
    count = 0
    while 1:
        print("b")
        count += 1
        if count > 10000:
            break


if __name__ == '__main__':
    Process(target=loopa).start()
    Process(target=loopb).start()