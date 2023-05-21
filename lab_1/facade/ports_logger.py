from random import choice
from os import environ
from aiohttp import ClientSession, ClientError


class LoggerPorts:
    proxys_servies = [
        f"http://api-loggin-1:{environ.get('PORT_LOGGER_1')}",
        f"http://api-loggin-2:{environ.get('PORT_LOGGER_2')}",
        f"http://api-loggin-3:{environ.get('PORT_LOGGER_3')}"
    ]
    
    @classmethod
    async def choose_service(cls) -> str:
        while True:
            choosen_serv = choice(cls.proxys_servies)
            try:
                await cls.get_massage_from_service(url=choosen_serv, method="GET")
                return choosen_serv
            except ClientError:
                print("Chosen service not work {}".format(choosen_serv)) 
                
    @staticmethod
    async def get_massage_from_service(url: str, method: str, json: dict = None) -> dict:
        async with ClientSession(url) as session:
            async with session.request(url="/", method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()
