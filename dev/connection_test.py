class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        else:
            print("Warning. Instance of PingPongThread is singleton. You cannnot change arguments.")
        return cls._instances[cls]
    # def __del__(self):
    #     self._instances = None

class xx(metaclass=SingletonMeta):
    def __init__(self) -> None:
        pass

    @classmethod
    def remove(cls):
        cls.__class__._instances = {}
    
    def remove2(self):
        xx.remove()


gg = xx()

gg.remove2()
del gg

hh = xx()