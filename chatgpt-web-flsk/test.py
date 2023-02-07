import threading


class A(object):
    _instance = None
    _lock = threading.Lock()

    _instance1 = 1

    instance2 = 2

    def instance(self):
        return 1

    @classmethod
    def instanceclass(cls):
        return cls.instance2

    @classmethod
    def get_instance(cls, ins_name):
        """
        实现单例模式
        """
        if cls._instance is not None:
            return cls._instance

        with cls._lock:
            if cls._instance is not None:
                return cls._instance

            cls._instance = ins_name()
            return cls._instance


class B(A):
    a = 10

    def p(self):
        print(f"Starting {self.a}")


class C(A):
    a = 20

    def p(self):
        print(f"Starting {self.a}")


if __name__ == '__main__':
    b = B.get_instance(B)
    c = C.get_instance(C)
    b.p()
    c.p()
