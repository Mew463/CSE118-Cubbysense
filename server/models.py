from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    in_cubby: Optional[int] = Field(default=None, index=True)

class AlexaRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    request_type: str
    intent_name: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
class AlexaRequestBase(BaseModel):
    version: str
    session: dict
    request: dict
    context: dict

class ItemCreate(BaseModel):
    item_name: str
    cubby_number: int
