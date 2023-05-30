from fastapi import FastAPI
from get_message_from_facade import GetMessageFromFacade
from base_client import MapHz


app = FastAPI()
MapHz(
    list_nodes=[
        "hazelcast-node-1:5701", 
        "hazelcast-node-2:5701", 
        "hazelcast-node-3:5701"
        ], 
    cluster_name="dev",
    name_map="hash_map"
    )


@app.get("/")
async def get_message(): 
    out_from_table = MapHz().map_hz.values().result() if MapHz().map_hz.size().result() else "Not Found Data"
    print("Message {}".format(out_from_table))
    return {"Response": out_from_table}
        

@app.post("/")
async def save_message(data: GetMessageFromFacade):
    MapHz().send_data(unique_id=data.uuid, massange=data.message)
    print("Message id = {}\nmessgae = {}".format(data.uuid, data.message))
    return {"Response": data.message}
