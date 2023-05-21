from fastapi import FastAPI, BackgroundTasks
from modal_body import GetMessage
import uuid
from ports_logger import FabricService
from base_client import WithQuiene


app = FastAPI()


@app.get("/")
async def plus_strings():
    logger_service, message_servce = await FabricService.get_each_serivce()
    
    tmp = 'message = '
    for messgae_from_log in (await message_servce.get_massage_from_service()).get("Response"):
        tmp += "{}\n".format(messgae_from_log)
    
    tmp += 'logger = '  
    for messgae_from_log in (await logger_service.get_massage_from_service()).get("Response"):
        tmp += "{}\n".format(messgae_from_log)

    return {"Response": "{}".format(
        tmp
        )}


@app.post("/")
async def save_message(data: GetMessage):
    logger_service, _ = await FabricService.get_each_serivce()
    
    await logger_service.get_massage_from_service(
        method="POST",
        json={
           "message": data.message,
           "uuid": str(uuid.uuid4())
        }
    )
    
    with WithQuiene(**{
        "list_nodes":[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
        "cluster_name":"dev",
        "name_quiene": "massange_qu"
    }) as queue_dist:
        queue_dist.put(data.message)
        
    return {"Response": data.message}
