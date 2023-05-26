from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_message():

    return {"Response": "Not Implemented"}


