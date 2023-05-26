from hazelcast import HazelcastClient
from dataclasses import dataclass, field
from singltone import Singltone


@dataclass
class ClientOperator(metaclass=Singltone):
    list_nodes: list
    cluster_name: str
    name_map: str = field(default="")
    name_quiene: str = field(default="")
    
    def __post_init__(self):
        self._client = HazelcastClient(
            cluster_name=self.cluster_name, 
            cluster_members=self.list_nodes
            )
    

class MapHz(ClientOperator):
    
    def __post_init__(self):
        super().__post_init__()
        self._map_dist = self._client.get_map(self.name_map)
        
    @property
    def map_hz(self):
        return self._map_dist
    
    def send_data(self, unique_id: str, massange: str) -> str:
        self.map_hz.set(unique_id, massange).result()
        return self.map_hz.get(unique_id).result()
    

class QuieneHz(ClientOperator):
    
    def __post_init__(self):
        super().__post_init__()
        self._quiene_hz = self._client.get_queue(self.name_quiene)
        
    @property
    def quiene_hz(self):
        return self.quiene_hz
