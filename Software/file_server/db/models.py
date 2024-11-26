from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    in_cubby: Optional[int] = Field(default=None, index=True)

class ItemCreate(BaseModel):
    name: str
    in_cubby: int

class LED(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    color: str

class LEDUpdate(BaseModel):
    color: str
    id: int
