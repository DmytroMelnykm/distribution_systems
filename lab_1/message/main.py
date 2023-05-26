from fastapi import FastAPI
from base_client import QuieneHz
from asyncio import create_task, sleep
from hazelcast.proxy.queue import BlockingQueue
from singltone import ListMessages


app = FastAPI()


async def get_and_check_element(queue: BlockingQueue):
    if (element := queue.poll()) is None:
        return await sleep(2)
    
    ListMessages().messages.append(element)
    await sleep(2)


async def check_massage():
    QuieneHz(list_nodes=[
            "hazelcast-node-1:5701", 
            "hazelcast-node-2:5701", 
            "hazelcast-node-3:5701"
            ], 
        cluster_name="dev",
        name_quiene="massange_qu"
        )
    QUIENE_HZ = QuieneHz().quiene_hz
    while True:
        await get_and_check_element(QUIENE_HZ)
                

@app.on_event("startup")
async def startup_event():
    ListMessages()
    task = create_task(check_massage()) 


@app.get("/")
async def get_message():
    print(str(ListMessages()))
    return {"Response": ListMessages().messages}
