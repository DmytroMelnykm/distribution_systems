from fastapi import FastAPI
from base_client import QuieneHz
from asyncio import create_task, sleep
from singltone import ListMessages
from consul import Consul, Check
from os import environ


app = FastAPI()


async def check_massage():
    while True:
        await QuieneHz().get_and_check_element()

    
@app.on_event("startup")
async def startup_event():
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
    await QuieneHz( 
        cluster_name="dev",
        name_quiene="massange_qu"
    ).get_client()
    ListMessages()
    task = create_task(check_massage()) 


@app.get("/")
async def get_message():
    print(str(ListMessages()))
    return {"Response": ListMessages().messages}


@app.get("/check/counsul/")
async def plus_strings():
    return {"Response": "OK"}
