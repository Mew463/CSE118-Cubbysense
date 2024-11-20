from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
import logging
from pydantic import BaseModel

from .services import ItemService, get_item_service

router = APIRouter()
logger = logging.getLogger(__name__)

class ItemCreate(BaseModel):
    name: str
    in_cubby: int

@router.get("/")
async def read_root():
    return {"Hello": "World"}

@router.get("/items")
async def get_items(item_service: ItemService = Depends(get_item_service)):
    items = await item_service.read_all_items()
    return {"items": items}

@router.post("/items")
async def create_item(
    item_data: ItemCreate,  # Use Pydantic model
    item_service: ItemService = Depends(get_item_service)
):
    await item_service.create_item(name=item_data.name, cubby_number=item_data.in_cubby)
    return {"message": f"Item {item_data.name} created"}

@router.delete("/items/{id}")
async def delete_item_by_id(
    id: int,
    item_service: ItemService = Depends(get_item_service)
):
    deleted = await item_service.delete_item(item_id=id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Item with ID {id} not found")
    return {"message": f"Item with ID {id} deleted"}

@router.delete("/items")
async def delete_item_by_name(
    name: Optional[str] = None,
    item_service: ItemService = Depends(get_item_service)
):
    if not name:
        raise HTTPException(status_code=400, detail="Query parameter 'name' is required")
    deleted = await item_service.delete_item_by_name(name)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Item with name '{name}' not found")
    return {"message": f"Item '{name}' deleted"}
