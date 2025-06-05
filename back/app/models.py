from pydantic import BaseModel, ConfigDict


class Question(BaseModel):
    text: str
