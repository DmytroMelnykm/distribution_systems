from pydantic import BaseModel


class GetMessageFromFacade(BaseModel):
    message: str
    uuid: str