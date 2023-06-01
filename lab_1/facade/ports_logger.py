from random import choice
from os import environ
from aiohttp import ClientSession, ClientError
from dataclasses import dataclass


@dataclass
class ServicesPorts:
    proxys_servies: list[str]
    
    async def choose_service(self) -> str:
        while True:
            self.__choosen_serv = choice(self.proxys_servies)
            try:
                await self.get_massage_from_service(method="GET")
                return 
            except ClientError:
                print("Chosen service not work {}".format(self.__choosen_serv)) 
                
    async def get_massage_from_service(self, method: str = "GET", url: str = "/", json: dict = None) -> dict:
        async with ClientSession(self.service) as session:
            async with session.request(url=url, method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()
    
    @property
    def service(self):
        return self.__choosen_serv
            

class FabricService:
    
    @classmethod
    def get_service_logger(cls) -> ServicesPorts:
        return ServicesPorts(proxys_servies=[
            f"http://api-loggin-1:{environ.get('PORT_LOGGER_1')}",
            f"http://api-loggin-2:{environ.get('PORT_LOGGER_2')}",
            f"http://api-loggin-3:{environ.get('PORT_LOGGER_3')}"
        ])  
    
    @classmethod
    def get_service_message(cls) -> ServicesPorts:
        return ServicesPorts(proxys_servies=[
            f"http://api-message-1:{environ.get('PORT_MESSAGE_1')}",
            f"http://api-message-2:{environ.get('PORT_MESSAGE_2')}"
        ])
    
    @staticmethod
    async def choosen_services(services: list[ServicesPorts]):
        for service in services:
            await service.choose_service()
        
    @classmethod
    async def get_each_serivce(cls):
        services = (
            cls.get_service_logger(), 
            cls.get_service_message()
            )
        await cls.choosen_services(services)
        return services
