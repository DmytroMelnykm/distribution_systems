from fastapi import FastAPI
from base_client import QuieneHz
from asyncio import create_task, sleep
from hazelcast.proxy.queue import BlockingQueue
from singltone import ListMessages


app = FastAPI()
QuieneHz(list_nodes=[
        "hazelcast-node-1:5701", 
        "hazelcast-node-2:5701", 
        "hazelcast-node-3:5701"
        ], 
    cluster_name="dev",
    name_quiene="massange_qu"
    )


async def check_massage():
    while True:
        await QuieneHz().get_and_check_element()
                

@app.on_event("startup")
async def startup_event():
    ListMessages()
    task = create_task(check_massage()) 


@app.get("/")
async def get_message():
    print(str(ListMessages()))
    return {"Response": ListMessages().messages}
