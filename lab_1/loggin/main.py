from fastapi import FastAPI
from get_message_from_facade import GetMessageFromFacade
from base_client import ClientOperator


app = FastAPI()


@app.get("/")
async def save_message(): 
    
    return {"Response": ""}


@app.post("/")
async def save_message(data: GetMessageFromFacade):
    
    enter_param = {
        "list_nodes":[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
        "cluster_name":"dev",
        "name_map": "hash_map"
    }
    
    with ClientOperator(**enter_param) as map_dist:
        ClientOperator.send_data(
            map_dist=map_dist, 
            unique_id=data.uuid,
            massange=data.message
            )
        #print(f"key = {key}, value = {value}")
    
    return {"Response": data.message}
