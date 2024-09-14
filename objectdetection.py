import cv2
from ultralytics import YOLO
import pyttsx3
import time

def object_detection(model):
    # Text-to-Speech engine initialization
    engine = pyttsx3.init()

    # Set the interval for reading objects (in seconds)
    reading_interval = 2
    last_read_time = time.time()

    # Perform object detection using the YOLO model
    results = model(source="0", stream=True, show=True)  # Results is a generator object
    for r in results:
        current_time = time.time()
        if current_time - last_read_time >= reading_interval:
            boxes = r.boxes  # Boxes object for bounding box outputs
            labels = r.names  # Labels for the detected objects
            # Loop through the detected boxes and read out the object names
            for box in boxes:
                class_id = int(box.cls)
                label = labels[class_id]
                print(f"Detected: {label}")
                engine.say(label)
                engine.runAndWait()
            # Update the last read time
            last_read_time = current_time
        # Terminate the loop by pressing the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break  # Break the loop
