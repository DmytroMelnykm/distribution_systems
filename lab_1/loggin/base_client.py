from hazelcast import HazelcastClient
from dataclasses import dataclass, field
from uuid import uuid4



@dataclass
class ClientOperator:
    list_nodes: list
    cluster_name: str
    name_map: str = field(default="")
    name_quiene: str = field(default="")
    
    def __post_init__(self):
        self.client = HazelcastClient(
            cluster_name=self.cluster_name, 
            cluster_members=self.list_nodes
            )
    
    def __enter__(self):
        map_dist = self.client.get_map(self.name_map).blocking()
        return map_dist
            
    
    def __exit__(self, type, value, traceback):
        self.client.shutdown()

    @staticmethod
    def send_data(map_dist, unique_id: str, massange: str) -> str:
        map_dist.set(unique_id, massange)
        return map_dist.get(unique_id)
    

class WithQuiene(ClientOperator):
    
    def __enter__(self):
        return self.client.get_queue(self.name_quiene).blocking()
            
    
    def __exit__(self, type, value, traceback):
        self.client.shutdown()