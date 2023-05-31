from fastapi import FastAPI
from modal_body import GetMessage
import uuid
from ports_logger import FabricService
from base_client import QuieneHz
from consul import Consul, Check
from os import environ


app = FastAPI()

@app.on_event("startup")
async def register_service():
    consul = Consul(host="consul-service", port=int(environ.get("PORT_CONSUL"))) 
    service_id = environ.get('PROXY_SERVICE') 
    service_name = environ.get('PROXY_SERVICE')
    service_port = int(environ.get('PORT_SEVICE'))

    check = Check.http(f"http://api-facade:{environ.get('PORT_SEVICE')}/check/counsul/", interval="10s")  

    consul.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=environ.get('PROXY_SERVICE'),  # Имя сервиса, указанное в Docker Compose
        port=service_port,
        check=check,
        timeout="30s"
    )
    await QuieneHz(
        cluster_name="dev",
        name_quiene="massange_qu"
        ).get_client()




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
    await QuieneHz().send_data(data.message)
    return {"Response": data.message}


@app.get("/check/counsul/")
async def plus_strings():
    return {"Response": "OK"}

