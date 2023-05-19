from random import choice
from os import environ


class LoggerPorts:
    proxys_servies = [
        f"http://api-loggin-1:{environ.get('PORT_LOGGER_1')}",
        f"http://api-loggin-2:{environ.get('PORT_LOGGER_2')}",
        f"http:/api-loggin-3:{environ.get('PORT_LOGGER_3')}"
    ]
    
    @classmethod
    def choose_service(cls):
        return choice(cls.proxys_servies)
