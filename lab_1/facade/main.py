from fastapi import FastAPI
from modal_body import GetMessage
import uuid
from ports_logger import FabricService
from base_client import QuieneHz
from consul import Consul


app = FastAPI()

# @app.on_event("startup")
# async def register_service():
#     consul = Consul(host="consul-service", port=8500)  # Подставьте правильные значения хоста и порта Consul
#     service_id = "api-facade"  # Уникальный идентификатор вашего сервиса
#     service_name = "api-facade"  # Имя вашего сервиса
#     service_port = 8015  # Порт, на котором работает ваш сервис

#     check = Consul.Check.http(f"http://api-facade:{service_port}/")  # Путь к эндпоинту проверки состояния вашего сервиса

#     consul.agent.service.register(
#         name=service_name,
#         service_id=service_id,
#         address="api-facade",  # Имя сервиса, указанное в Docker Compose
#         port=service_port,
#         check=check
#     )

QuieneHz(
    list_nodes=[
        "hazelcast-node-1:5701", 
        "hazelcast-node-2:5701", 
        "hazelcast-node-3:5701"
        ], 
    cluster_name="dev",
    name_quiene="massange_qu"
)


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
