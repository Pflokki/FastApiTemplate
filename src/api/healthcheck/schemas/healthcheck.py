from pydantic import BaseModel


class ReadyItem(BaseModel):
    service: str
    status: str = 'alive'
