import time


def t(func):
    start = time.time()
    def wrap():
        func()
        end = time.time()
        print("耗费时间为：%s" % (end-start))
    return wrap



@t
def fool():
    for _ in range(1000000):
        pass


if __name__ == "__main__":
    for i in range(2):
        pass
    fool()