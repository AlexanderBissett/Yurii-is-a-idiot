
def singleton(cls):
    instances = {}
    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance

def work(cc):
    cc.cnt = 16

@singleton
class CustomCounter():

    def __init__(self, val = 10):
        self.__cnt = val

    @property
    def cnt(self):
        return self.__cnt
    
    @cnt.setter
    def cnt(self, val):
        self.__cnt = val
    

if __name__ == '__main__':
    cc = CustomCounter()
    print(cc)
    cc.cnt = 13
    cc_copy = CustomCounter()
    print(cc_copy)
    work(cc_copy)
    print(cc_copy)