class Singltone(type):
    __instances_set = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances_set:
            cls.__instances_set[cls] = super(Singltone, cls).__call__(*args, **kwargs)
        return cls.__instances_set[cls]
