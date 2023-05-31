from fastapi import FastAPI
from get_message_from_facade import GetMessageFromFacade
from base_client import MapHz
from consul import Consul, Check
from os import environ

app = FastAPI()


@app.on_event("startup")
async def register_service():
    consul = Consul(host="consul-service", port=int(environ.get("PORT_CONSUL"))) 
    service_id = environ.get('PROXY_SERVICE') 
    service_name = environ.get('PROXY_SERVICE') 
    service_port = int(environ.get('PORT_SEVICE'))

    check = Check.http(f"http://{environ.get('PROXY_SERVICE')}:{environ.get('PORT_SEVICE')}/check/counsul/", interval="10s")

    consul.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=environ.get('PROXY_SERVICE'),  
        port=service_port,
        check=check,
        timeout="30s"
    )


MapHz(
    list_nodes=[
        "hazelcast-node-1:5701", 
        "hazelcast-node-2:5701", 
        "hazelcast-node-3:5701"
        ], 
    cluster_name="dev",
    name_map="hash_map"
    )


@app.get("/check/counsul/")
async def plus_strings():
    return {"Response": "OK"}


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
