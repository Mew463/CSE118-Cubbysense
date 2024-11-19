import logging
from services import ItemService
from models import AlexaRequest

logger = logging.getLogger(__name__)

class AlexaRequestController:
    def __init__(self, item_service: ItemService):
        self.item_service = item_service

    def build_response(self, message, end_session=False):
        return {
            "version": "1.0",
            "response": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": message
                },
                "shouldEndSession": end_session
            }
        }

    async def handle_launch_request(self):
        return self.build_response("Welcome to the CubbySense skill. You can ask me to add, remove, or update items in your list.")

    async def handle_bye_intent(self, confirmed=False):
        items_in_cubby = await self.item_service.read_all_items_in_cubby()
        if items_in_cubby and not confirmed:
            string_items = ", ".join([item.name for item in items_in_cubby])
            return self.build_response(f"You still have {string_items} in your cubbies. Are you sure you don't need them?")
        return self.build_response("You are all set, goodbye! Have a great day.", True)

    async def handle_get_items_intent(self):
        items_in_cubby = await self.item_service.read_all_items_in_cubby()
        items_not_in_cubby = await self.item_service.read_all_items_not_in_cubby()
        in_cubby_names = ", ".join([item.name for item in items_in_cubby])
        not_in_cubby_names = ", ".join([item.name for item in items_not_in_cubby])
        response_message = f"Items in cubbies: {in_cubby_names}. Items not in cubbies: {not_in_cubby_names}."
        return self.build_response(response_message)

    async def handle_find_item_intent(self, item_name):
        items = await self.item_service.read_all_items_in_cubby()
        item = next((i for i in items if i.name == item_name), None)
        if item:
            status = f"in cubby number {item.in_cubby}" if item.in_cubby is not None else "not in cubby"
            return self.build_response(f"{item_name} is currently {status}.")
        return self.build_response(f"Could not find {item_name} in your list.")

    async def handle_help_intent(self):
        return self.build_response("You can ask me to add, remove, or check the status of items in your cubbies.")
    
    # async def handle_add_item_intent(self, item_name):
    #     if not item_name:
    #         return self.build_response("Sorry, I didn't catch the item name.")
    #     await self.item_service.create_item(name=item_name)
    #     return self.build_response(f"I have added {item_name} to your list.")

    # async def handle_remove_item_intent(self, item_name):
    #     if not item_name:
    #         return self.build_response("Sorry, I didn't catch the item name.")
    #     items = await self.item_service.read_all_items_in_cubby()
    #     item = next((i for i in items if i.name == item_name), None)
    #     if item:
    #         await self.item_service.delete_item(item_id=item.id)
    #         return self.build_response(f"I have removed {item_name} from your list.")
    #     return self.build_response(f"Could not find {item_name} in your list.")

