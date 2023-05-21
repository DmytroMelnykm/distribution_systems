from fastapi import FastAPI
from get_message_from_facade import GetMessageFromFacade
from base_client import ClientOperator


app = FastAPI()


@app.get("/")
async def get_message(): 
    with ClientOperator(**{
        "list_nodes":[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
        "cluster_name":"dev",
        "name_map": "hash_map"
    }) as map_dist:
        
        out_from_table = map_dist.values() if map_dist.size() else "Not Found Data"
        print("Message {}".format(out_from_table))
        return {"Response": out_from_table}
        
    
    


@app.post("/")
async def save_message(data: GetMessageFromFacade):
    
    with ClientOperator(**{
        "list_nodes":[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
        "cluster_name":"dev",
        "name_map": "hash_map"
    }) as map_dist:
        ClientOperator.send_data(
            map_dist=map_dist, 
            unique_id=data.uuid,
            massange=data.message
            )
        print("Message id = {}\nmessgae = {}".format(data.uuid, data.message))
    
    return {"Response": data.message}
