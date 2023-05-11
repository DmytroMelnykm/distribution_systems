from fastapi import FastAPI
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()


@app.get("/")
async def get_message():

    return {"Response": "Not Implemented"}


