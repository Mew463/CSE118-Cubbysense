# import sqlite3

# # Create a new SQLite database (or connect if it exists)
# conn = sqlite3.connect('detected_objects.db')
# cursor = conn.cursor()

# # Create a table to store detected objects
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS objects (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         label TEXT,
#         x INTEGER,
#         y INTEGER,
#         width INTEGER,
#         height INTEGER,
#         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
# ''')

# Commit and close the connection
#conn.commit()
#conn.close()

# import sqlite3
import cv2
import numpy as np
import requests

# Function to add detected objects to the database

def add_or_update_object(label, x, y, width, height):
    # decide for the cubby 
    threshold = 0
    cubby = 0
    ## TODO define realistic threshold for cubbies 
    if x < threshold: 
        if y < threshold: 
            cubby = 0
        else: 
            cubby = 1
    else: 
        if y < threshold: 
            cubby = 2
        else: 
            cubby = 3            
    current_object = {
        "name": label,
        "in_cubby": cubby
    }
    response = requests.post(url="http://localhost:8000/items", json=current_object)
    # Check and handle the response
    if response.status_code == 200:
        print("Success:", response.json())
    elif response.status_code == 404:
        print("Not Found:", response.json())
    else:
        print("Error:", response.status_code, response.text)
    
    # # conn = sqlite3.connect('detected_objects.db')
    # # cursor = conn.cursor()

    # # Check if object already exists (based on label and coordinates)
    # cursor.execute('''
    #     SELECT id FROM objects
    #     WHERE label = ? AND x = ? AND y = ? AND width = ? AND height = ?
    # ''', (label, x, y, width, height))

    # existing_object = cursor.fetchone()

    # if existing_object:
    #     # Update timestamp if object already exists
    #     cursor.execute('''
    #         UPDATE objects
    #         SET timestamp = CURRENT_TIMESTAMP
    #         WHERE id = ?
    #     ''', (existing_object[0],))
    # else:
    #     # Insert new object if not found in the database
    #     cursor.execute('''
    #         INSERT INTO objects (label, x, y, width, height)
    #         VALUES (?, ?, ?, ?, ?)
    #     ''', (label, x, y, width, height))

    # Commit and close the connection
    # conn.commit()
    # conn.close()
    
#add_or_update_object("Key", 1,1, 150, 150)


# Function to delete objects that are no longer detected
def remove_missing_objects(current_objects):
    # Define the endpoint URL
    # Send the DELETE request
    response = requests.delete(f"/items/{current_objects}")

    # Check and handle the response
    if response.status_code == 200:
        print("Success:", response.json())
    elif response.status_code == 404:
        print("Not Found:", response.json())
    else:
        print("Error:", response.status_code, response.text)
    
    
    # conn = sqlite3.connect('detected_objects.db')
    # cursor = conn.cursor()

    # Fetch all objects currently in the database
    # cursor.execute('SELECT id, label, x, y, width, height FROM objects')
    # db_objects = cursor.fetchall()

    # # Remove objects that are no longer detected
    # for db_obj in db_objects:
    #     if db_obj not in current_objects:
    #         cursor.execute('DELETE FROM objects WHERE id = ?', (db_obj[0],))

    # conn.commit()
    # conn.close()


# Load YOLOv3 model with COCO classes
YOLO_CONFIG = 'yolov3.cfg'
YOLO_WEIGHTS = 'yolov3.weights'
LABELS_FILE = 'coco.names'

with open(LABELS_FILE, 'r') as f:
    labels = f.read().strip().split('\n')

net = cv2.dnn.readNetFromDarknet(YOLO_CONFIG, YOLO_WEIGHTS)
cap = cv2.VideoCapture(0) # 0 for webcam and 1 for external cam 

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

while True:
    import time 
    time.sleep(1)

    ret, image = cap.read()
    if not ret:
        print("Error: Failed to grab frame.")
        break

    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    outs = net.forward(output_layers)

    current_objects = []  # List to store current detected objects

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                label = labels[class_id]

                # Add or update the detected object in the database
                add_or_update_object(label, x, y, w, h)

                # Track current detected objects (used for removal of missing objects)
                current_objects.append((label, x, y, w, h))

                # Draw bounding box and label on image
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #cv2.imwrite("output_yolo.jpg", image)

    # Print detected items
    print("Detected items:", current_objects)

    # Remove objects that are no longer detected
    remove_missing_objects(current_objects)

    # Show the output image with bounding boxes
    #cv2.imshow("Output", image)

    # Wait for 'q' to quit the loop
    #key = cv2.waitKey(1) & 0xFF
    #if key == ord('q'):
     #   break

cap.release()
#cv2.destroyAllWindows()
