from pydantic import BaseModel


class GetMessage(BaseModel):
    message: str