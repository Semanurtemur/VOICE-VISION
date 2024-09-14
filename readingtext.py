import cv2
import pytesseract
import pyttsx3
import time

def read_text_from_camera():
    # Specify the Tesseract OCR path
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

    # Capture video from the camera
    camera = cv2.VideoCapture(0)

    # Start time
    start_time = time.time()

    # Reading interval (in seconds)
    reading_interval = 3

    while True:
        # Capture a frame from the camera
        ret, frame = camera.read()

        # Break the loop if a frame cannot be captured
        if not ret:
            print("Failed to capture frame from the camera.")
            break

        # Read text at specific intervals
        if time.time() - start_time >= reading_interval:
            # Read text from the frame
            text = pytesseract.image_to_string(frame)

            # Print the text to the console
            print(text)

            # Read the text aloud
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()

            # Update the start time
            start_time = time.time()

        # Show the frame
        cv2.imshow("Camera", frame)

        # Terminate the loop by pressing the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera
    camera.release()
    cv2.destroyAllWindows()
