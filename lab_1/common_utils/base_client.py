from hazelcast import HazelcastClient
from dataclasses import dataclass, field
from singltone import Singltone, ListMessages
from hazelcast.proxy.queue import Queue
from asyncio import sleep
from aiohttp import ClientSession
from typing import ClassVar


@dataclass
class ClientOperator(metaclass=Singltone):
    cluster_name: str
    name_map: str = field(default="")
    name_quiene: str = field(default="")
    service_counsul: ClassVar[str] = "http://consul-service:8500"
    
    
    async def get_client(self):
        list_nodes = await self.get_adress_nodes()
        self._client = HazelcastClient(
            cluster_name=self.cluster_name, 
            cluster_members=list_nodes
            )
    
    async def get_adress_nodes(self):
        list_nodes = []
        for number_serv in range(3):
            info_service = await self.__get_service_name(
                url="/v1/catalog/service/{service_name}".format(
                    consul=self.service_counsul,
                    service_name= "hazelcast-node-{}".format(number_serv + 1)
            ))
            info_service = info_service[0]
            list_nodes.append("{addres}:{ports}".format(
                addres=info_service["ServiceName"],
                ports=info_service["ServicePort"]
                )) 
        return list_nodes
    
    async def __get_service_name(self, method: str = "GET", url: str = "/", json: dict = None) -> dict:
        async with ClientSession("http://consul-service:8500") as session:
            async with session.request(url=url, method=method, json=json) as response:
                response.raise_for_status()
                return await response.json()
    

class MapHz(ClientOperator):
    
    async def get_client(self):
        await super().get_client()
        self._map_dist = self._client.get_map(self.name_map)
        
    @property
    def map_hz(self):
        return self._map_dist
    
    def send_data(self, unique_id: str, massange: str) -> str:
        self.map_hz.set(unique_id, massange).result()
        return self.map_hz.get(unique_id).result()
    

class QuieneHz(ClientOperator):
    
    async def get_client(self):
        await super().get_client()
        self._quiene_hz_create = self._client.get_queue(self.name_quiene)
        
    @property
    def quiene_hz(self) -> Queue:
        return self._quiene_hz_create
    
    async def send_data(self, message: str):
        self.quiene_hz.put(message).result()
    
    async def get_and_check_element(self):
        if (element := self.quiene_hz.poll().result()) is None:
            return await sleep(1)
        ListMessages().messages.append(element)
        await sleep(1)
