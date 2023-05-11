from fastapi import FastAPI
from get_message_from_facade import GetMessageFromFacade

app = FastAPI()
hash_table = {}


@app.get("/")
async def save_message(): 
    
    return {"Response": list(hash_table.values())}


@app.post("/")
async def save_message(data: GetMessageFromFacade):
    if hash_table.get(data.uuid, None):
        return {"Response": "Bad uuid"}
    
    hash_table[data.uuid] = data.message
    print(hash_table) 
    
    return {"Response": data.message}


