from pydantic import BaseModel


class AliveData(BaseModel):
    data: str
