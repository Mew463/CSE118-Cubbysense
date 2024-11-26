# File Server

## Starting Server

To start the server, run the following command:

```bash
cd Software/file_server && uvicorn server:app --reload
```

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

### DELETE /items/cubby/{cubby_number}

Deletes all items in a cubby by its number.

Parameters:

    cubby_number: (int) The number of the cubby to be emptied.

Example Request:

DELETE /items/cubby/1

Response:

    Returns a message confirming the deletion of all items in the cubby.

Example Response:
```json
{
  "message": "Items in cubby 1 deleted"
}
```

### GET /leds

Retrieves the status of all LEDs.

Response:

    Returns a list of LEDs and their status.

Example Response:
```json
{
  "leds": [
    {"id": 1, "color": "off"},
    {"id": 2, "color": "green"}
  ]
}
```

### PUT /leds/{id}

Updates the status of an LED by its id.

Parameters:

    id: (int) The id of the LED to be updated.

Body:

    color: (string) The new color of the LED.
    id: (int) The id of the LED to be updated.
  

Example Request:

PUT /leds/1
```json
{
  "color": "pink",
  "id": 1
}
```

Response:

    Returns a message confirming the LED's update.

Example Response:
```json
{
    "led": {
        "id": 1,
        "color": "pink"
    }
}
```


Using SQL:

# PostgreSQL Quick Start Commands

## 1. Start/Stop PostgreSQL
```bash
# Start PostgreSQL (Linux/macOS)
sudo systemctl start postgresql

# Stop PostgreSQL
sudo systemctl stop postgresql

# Check Status
sudo systemctl status postgresql
```

## 2. Access PostgreSQL Command Line Interface (CLI)
```bash
# Connect as default `postgres` user
psql -U postgres
```

## 3. Create a New Database
```sql
-- Inside the `psql` CLI
CREATE DATABASE my_database;
```

## 4. List Databases
```sql
-- Inside `psql`
\l
```

## 5. Switch to a Database
```sql
-- Inside `psql`
\c my_database
```

## 6. Create a Table
```sql
-- Example table creation
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100)
);
```

## 7. Insert Data
```sql
-- Insert rows into a table
INSERT INTO users (name, email) VALUES ('John Doe', 'john@example.com');
```

## 8. View Data
```sql
-- Query all rows
SELECT * FROM users;
```

## 9. List Tables
```sql
-- Inside `psql`
\dt
```

## 10. Exit psql
```bash
# Simply type:
\q
```


