from dataclasses import dataclass
from typing import ClassVar


class Singltone(type):
    __instances_set = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances_set:
            cls.__instances_set[cls] = super(Singltone, cls).__call__(*args, **kwargs)
        return cls.__instances_set[cls]
    

@dataclass 
class ListMessages(metaclass=Singltone):
    __list_messages: ClassVar = []
    
    def __str__(self) -> str:
        tmp_messages = ""
        for count, messeg in enumerate(self.messages):
            tmp_messages += "numer = {} message = {}\n".format(count, messeg)
            
        return tmp_messages
    
    @property
    def messages(self) -> list:
        return self.__list_messages
