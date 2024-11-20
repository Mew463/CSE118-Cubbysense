from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    in_cubby: Optional[int] = Field(default=None, index=True)

class ItemCreate(BaseModel):
    item_name: str
    cubby_number: int
