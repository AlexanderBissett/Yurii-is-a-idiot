import cv2
import time
import threading

def showtime(image, event, a1, a2):
    print(a1)
    cv2.namedWindow(a2, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(a2, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(a2, image)

    while not event.is_set():
        print(a2)
        cv2.waitKey(1000)

path = r'C:\Users\udgo1\Downloads\10.png'
image = cv2.imread(path)

path2 = r'C:\Users\udgo1\Downloads\hg.png'
image2 = cv2.imread(path2)

event0 = threading.Event()
t0 = threading.Thread(target=showtime, args=(image, event0, 'hello', 'titi'))
t0.start()
time.sleep(2)
event0.set()
t0.join()

event1 = threading.Event()
t1 = threading.Thread(target=showtime, args=(image2, event1, 'goodbye', 'bianca'))
t1.start()
time.sleep(2)
event1.set()
t1.join()

cv2.destroyAllWindows()