import cv2
import numpy as np
import requests
from ultralytics import YOLO

host_ip = "192.168.0.141"
host_port = "8081"

last_cabinet_objects= []
cabinet_objects = []

# Function to add detected objects to the database

def add_or_update_object(label, cubby_index):  
    current_object = {
        "name": label,
        "in_cubby": cubby_index
    }
    response = requests.post(url=f"{host_ip}:{host_port}/items", json=current_object)
    # Check and handle the response
    if response.status_code == 200:
        print("Success:", response.json())
    elif response.status_code == 404:
        print("Not Found:", response.json())
    else:
        print("Error:", response.status_code, response.text)


# Function to delete objects that are no longer detected
def remove_missing_object(cubby_index):
    response = requests.delete(f"{host_ip}:{host_port}/items/{cubby_index}")

    # Check and handle the response
    if response.status_code == 200:
        print("Success:", response.json())
    elif response.status_code == 404:
        print("Not Found:", response.json())
    else:
        print("Error:", response.status_code, response.text)

# Load YOLOv3 model with COCO classes
YOLO_CONFIG = 'yolov3.cfg'
YOLO_WEIGHTS = 'yolov3.weights'
LABELS_FILE = 'coco.names'

with open(LABELS_FILE, 'r') as f:
    labels = f.read().strip().split('\n')

yolo = YOLO("yolov8s.pt")
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

    outs = yolo.track(image, stream=True)

    current_objects = []  # List to store current detected objects

    for out in outs:
        classes_names = out.names
        for box in out.boxes:
            # confidence check
            if box.conf[0] > 0.4:
                # coordinates
                [x1, y1, x2, y2] = box.xyxy[0]
                # convert to int
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                # get the class
                cls = int(box.cls[0])
                # get the class name
                class_name = classes_names[cls]
                # add_or_update_object(class_name, x1, y1, x2, y2)
                # draw the rectangle
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # put the class name and confidence on the image
                cv2.putText(image, f'{classes_names[int(box.cls[0])]} {box.conf[0]:.2f}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                current_objects.append(((classes_names[int(box.cls[0])]), x1, y1, x1-x2, y2-y1))
                
    
    cv2.imwrite("output_yolo.jpg", image)

    # Print detected items
    print("Detected items:", current_objects)

    bottom_left_cabinet_coords = [100, 600]
    top_right_cabinet_coords = [600, 100]
    object_size_limit = 100
    mid_cabinet_coords = [(top_right_cabinet_coords[0] - bottom_left_cabinet_coords[0])/2, (bottom_left_cabinet_coords[1] - top_right_cabinet_coords[1])/2]

    for object in cabinet_objects: # Make sure to erase the current array of cabinet_objects
        object = ""

    for object in current_objects:
        if (object[3] < object_size_limit and object[4] < object_size_limit): # Make sure the object is not really big 

            if (object[1] < mid_cabinet_coords[0] and object[1] > bottom_left_cabinet_coords[0] and object[2] > mid_cabinet_coords[1] and object[2] < top_right_cabinet_coords[1]): # Check Top left cabinet (from point of view of the camera)
                cabinet_objects[0] = object
                print("Item found in slot 1")
            elif (object[1] > mid_cabinet_coords[0] and object[1] < top_right_cabinet_coords[0] and object[2] > mid_cabinet_coords[1] and object[2] < top_right_cabinet_coords[1]): # Check Top right cabinet (from point of view of the camera)
                cabinet_objects[1] = object
                print("Item found in slot 2")
            elif (object[1] < mid_cabinet_coords[0] and object[1] > bottom_left_cabinet_coords[0] and object[2] < mid_cabinet_coords[1] and object[2] > bottom_left_cabinet_coords[1]): # Check bottom left cabinet (from point of view of the camera)
                cabinet_objects[2] = object
                print("Item found in slot 3")
            elif (object[1] > mid_cabinet_coords[0] and object[1] < top_right_cabinet_coords[0] and object[2] < mid_cabinet_coords[1] and object[2] > bottom_left_cabinet_coords[1]): # Check bottom right cabinet (from point of view of the camera)
                cabinet_objects[3] = object
                print("Item found in slot 4")

    for index, object_in_cabinet in enumerate(cabinet_objects):
        if object_in_cabinet != last_cabinet_objects[index]: # Cabinet object changed!!!
            if (object_in_cabinet == ""):
                remove_missing_object(index)
            else: 
                label = ''   # TODO
                add_or_update_object(label, index)
        
    last_cabinet_objects = cabinet_objects

    # Remove objects that are no longer detected
    # remove_missing_objects(current_objects)

    # Show the output image with bounding boxes
    #cv2.imshow("Output", image)

    # Wait for 'q' to quit the loop
    #key = cv2.waitKey(1) & 0xFF
    #if key == ord('q'):
     #   break

cap.release()
#cv2.destroyAllWindows()
