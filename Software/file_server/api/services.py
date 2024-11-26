from fastapi import HTTPException, Depends
from sqlmodel import Session, select
from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from db.models import Item, LED
from db.db_utils import get_session

class ItemService:
    def __init__(self, session: Session):
        self.session = session

    async def read_all_items(self) -> List[Item]:
        statement = select(Item)
        results = self.session.exec(statement).all()
        return results

    async def read_all_items_in_cubby(self) -> List[Item]:
        statement = select(Item).where(Item.in_cubby.isnot(None))
        results = self.session.exec(statement).all()
        return results

    async def read_all_items_not_in_cubby(self) -> List[Item]:
        statement = select(Item).where(Item.in_cubby == False)
        results = self.session.exec(statement).all()
        return results

    async def create_item(self, name: str, cubby_number: Optional[int] = None) -> Item:
        item = Item(name=name, in_cubby=cubby_number)
        self.session.add(item)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise HTTPException(status_code=400, detail="Item with this name already exists.")
        self.session.refresh(item)
        return item

    async def delete_item(self, item_id: int) -> None:
        item = self.session.get(Item, item_id)

        if not item:
            return False

        self.session.delete(item)
        self.session.commit()
        return True

    async def delete_items_by_cubby(self, cubby_number: int) -> None:
        statement = select(Item).where(Item.in_cubby == cubby_number)
        items = self.session.exec(statement).all()
        for item in items:
            self.session.delete(item)
        self.session.commit()
        return True
    
    async def delete_item_by_name(self, name: str) -> None:
        statement = select(Item).where(Item.name == name)
        item = self.session.exec(statement).first()

        if not item:
            return False

        self.session.delete(item)
        self.session.commit()
        return True

    async def update_item_status(self, item_id: int, in_cubby: bool) -> Item:
        item = self.session.get(Item, item_id)
        if not item:
            return
        item.in_cubby = in_cubby
        self.session.add(item)
        self.session.commit()
        return item
    

class LEDService:
    def __init__(self, session: Session):
        self.session = session

    async def create_led(self, color: str) -> LED:
        led = LED(color=color)
        self.session.add(led)
        self.session.commit()
        self.session.refresh(led)
        return led

    async def read_led(self, id: int) -> LED:
        led = self.session.get(LED, id)
        return led
    
    async def read_all_leds(self) -> List[LED]:
        statement = select(LED)
        results = self.session.exec(statement).all()
        return results

    async def update_led(self, id: int, color: str) -> LED:
        led = self.session.get(LED, id)
        if not led:
            return None
        led.color = color
        self.session.add(led)
        self.session.commit()

        updated_led = self.session.get(LED, id)
        return updated_led

    async def delete_led(self, id: int) -> None:
        led = self.session.get(LED, id)
        self.session.delete(led)
        self.session.commit()

# Dependency for ItemService
def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(session=session)

# Dependency for LEDService
def get_led_service(session: Session = Depends(get_session)) -> LEDService:
    return LEDService(session=session)