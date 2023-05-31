from random import choice
from os import environ
from aiohttp import ClientSession, ClientError
from dataclasses import dataclass
from typing import ClassVar
from asyncio import get_running_loop


@dataclass
class ServicesPorts:
    type_service: str
    count_services: int
    service_counsul: ClassVar[str] = "http://consul-service:8500"
    
    async def get_adress(self):
        self.proxys_servies = []
        match self.type_service:
            case "log":
                for number_serv in range(self.count_services):
                    info_service = await self.get_service_name(
                        url="/v1/catalog/service/{service_name}".format(
                            consul=self.service_counsul,
                            service_name= "api-loggin-{}".format(number_serv + 1)
                    ))
                    info_service = info_service[0]
                    self.proxys_servies.append("http://{addres}:{ports}".format(
                        addres=info_service["ServiceName"],
                        ports=info_service["ServicePort"]
                        ))
                    
            case "msg":
                for number_serv in range(self.count_services):
                    info_service = await self.get_service_name(
                        url="/v1/catalog/service/{service_name}".format(
                            consul=self.service_counsul,
                            service_name= "api-message-{}".format(number_serv + 1)
                    ))
                    info_service = info_service[0]
                    self.proxys_servies.append("http://{addres}:{ports}".format(
                        addres=info_service["ServiceName"],
                        ports=info_service["ServicePort"]
                        )) 
        
    
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
    
    async def get_service_name(self, method: str = "GET", url: str = "/", json: dict = None) -> dict:
        async with ClientSession("http://consul-service:8500") as session:
            async with session.request(url=url, method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()
    
    @property
    def service(self):
        return self.__choosen_serv
            

class FabricService:
    
    @classmethod
    async def get_service_logger(cls) -> ServicesPorts:
        logger = ServicesPorts(type_service="log", count_services=3)  
        await logger.get_adress()
        return logger
    
    @classmethod
    async def get_service_message(cls) -> ServicesPorts:
        message = ServicesPorts(type_service="msg", count_services=2)
        await message.get_adress()
        return message
    
    @staticmethod
    async def choosen_services(services: list[ServicesPorts]):
        for service in services:
            await service.choose_service()
        
    @classmethod
    async def get_each_serivce(cls):
        services = (
            await cls.get_service_logger(), 
            await cls.get_service_message()
            )
        await cls.choosen_services(services)
        return services
