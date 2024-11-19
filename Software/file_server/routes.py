from fastapi import APIRouter, Request, Depends
from services import ItemService, get_item_service
from alexa_request_controller import AlexaRequestController
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def read_root():
    return {"Hello": "World"}

@router.post("/items")
async def create_item(
    name: str,
    in_cubby: int | None,
    item_service: ItemService = Depends(get_item_service)
):
    await item_service.create_item(name=name, cubby_number=in_cubby)
    return {"message": f"Item {name} created"}

@router.delete("/items/{name}")
async def delete_item(
    name: str,
    item_service: ItemService = Depends(get_item_service)
):
    await item_service.delete_item_by_name(name)
    return {"message": f"Item {name} deleted"}

@router.post("/alexa_skill")
async def handle_alexa_request(
    request: Request,
    item_service: ItemService = Depends(get_item_service)
):
    alexa_request = await request.json()
    request_type = alexa_request["request"]["type"]
    logger.info("Request type: %s", request_type)
    intent_name = alexa_request["request"].get("intent", {}).get("name")
    logger.info("Intent name: %s", intent_name)
    slot_value = alexa_request["request"].get("intent", {}).get("slots", {}).get("ItemName", {}).get("value")
    controller = AlexaRequestController(item_service)

    if request_type == "LaunchRequest":
        return await controller.handle_launch_request()
    elif request_type == "IntentRequest":
        if intent_name == "AMAZON.HelpIntent":
            return await controller.handle_help_intent()
        elif intent_name == "AMAZON.YesIntent":
            return await controller.handle_bye_intent(confirmed=True) 
        elif intent_name == "ByeIntent":
            return await controller.handle_bye_intent()

        elif intent_name == "GetItemsIntent":
            return await controller.handle_get_items_intent()
        elif intent_name == "FindItemIntent":
            return await controller.handle_find_item_intent(slot_value)
        # elif intent_name == "AddItemIntent":
        #     return await controller.handle_add_item_intent(slot_value)
        # elif intent_name == "RemoveItemIntent":
        #     return await controller.handle_remove_item_intent(slot_value)
        else:
            return controller.build_response("Sorry, I didn't understand your intent.")
    else:
        return controller.build_response("Sorry, I didn't understand that request.")
