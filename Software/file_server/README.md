# File Server

## 

## Endpoints

### GET /

Returns a simple welcome message to confirm that the API is running.

Response:

{
  "Hello": "World"
}

### GET /items

Retrieves all items in the system.

Response:

    Returns a list of items in JSON format.

Example Response:
```json
{
  "items": [
    {"id": 1, "name": "Key", "in_cubby": 1, "id": 1},
    {"id": 2, "name": "Wallet", "in_cubby": 2, "id": 2}
  ]
}
```

### POST /items

Creates a new item with a name and a cubby number.

Parameters:

    name: (string) The name of the item.
    in_cubby: (integer) The cubby number where the item is stored.

Example Request:
```json
{
  "name": "Notebook",
  "in_cubby": 3
}
```

Response:

    Returns a message confirming the item's creation.

Example Response:
```json
{
  "message": "Item Notebook created"
}
```

### DELETE /items/{id}

Deletes an item by its id.

Parameters:

    id: (int) The id of the item to be deleted.

Example Request:

DELETE /items/1

Response:

    Returns a message confirming the item's deletion.

Example Response:
```json
{
  "message": "Item Key deleted"
}
```

### DELETE /items

Deletes an item by its name.

Query Parameters:

    name: (string) The name of the item to be deleted.

Example Request:

DELETE /items?name=Key

Response:

    Returns a message confirming the item's deletion.

Example Response:
```json
{
  "message": "Item 'Key' deleted"
}
```
