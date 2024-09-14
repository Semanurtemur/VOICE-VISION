import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
import speech_recognition as sr
from readingtext import read_text_from_camera
from objectdetection import object_detection
from ultralytics import YOLO


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("My Application")

        # Load the model
        self.model = YOLO('yolov8n.pt')

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)

        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Main frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Create instances of different pages
        for F in (StartPage,):
            frame = F(container, self, self.model)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

        # Exit button
        exit_image = Image.open("C:/Users/SEMANUR/PycharmProjects/pythonProject/venv/images/images.jpeg")
        exit_image = exit_image.resize((32, 32), Image.LANCZOS)
        self.exit_icon = ImageTk.PhotoImage(exit_image)
        exit_button = ttk.Button(self, image=self.exit_icon, command=self.quit)
        exit_button.pack(side="bottom", pady=10)

        # Announce options and listen for user input
        self.announce_options()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def announce_options(self):
        self.engine.say("Select the operation you want to perform. Say 1 for reading text from camera. Say 2 for object detection.")
        self.engine.runAndWait()
        self.listen_for_command()

    def listen_for_command(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            if "one" in command or "1" in command:
                read_text_from_camera()
            elif "two" in command or "2" in command:
                object_detection(self.model)
            else:
                self.engine.say("Sorry, I did not understand the command. Please say 1 for reading text from camera or 2 for object detection.")
                self.engine.runAndWait()
                self.listen_for_command()
        except sr.UnknownValueError:
            self.engine.say("Sorry, I did not catch that. Please say 1 for reading text from camera or 2 for object detection.")
            self.engine.runAndWait()
            self.listen_for_command()
        except sr.RequestError as e:
            self.engine.say(f"Could not request results; {e}")
            self.engine.runAndWait()

        self.ask_another_operation()

    def ask_another_operation(self):
        self.engine.say("Do you want to perform another operation? Say yes or no.")
        self.engine.runAndWait()

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            if "yes" in command:
                self.announce_options()
            elif "no" in command:
                self.engine.say("Thank you for using the application. Goodbye!")
                self.engine.runAndWait()
                self.quit()
            else:
                self.engine.say("Sorry, I did not understand the command. Please say yes or no.")
                self.engine.runAndWait()
                self.ask_another_operation()
        except sr.UnknownValueError:
            self.engine.say("Sorry, I did not catch that. Please say yes or no.")
            self.engine.runAndWait()
            self.ask_another_operation()
        except sr.RequestError as e:
            self.engine.say(f"Could not request results; {e}")
            self.engine.runAndWait()
            self.ask_another_operation()


class StartPage(tk.Frame):
    def __init__(self, parent, controller, model):
        super().__init__(parent)
        self.model = model

        # Logo
        logo_image = Image.open("C:/Users/SEMANUR/PycharmProjects/pythonProject/venv/images/VOICE VISION.jpg")
        logo_image = logo_image.resize((250, 250), Image.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_image)
        logo_label = tk.Label(self, image=logo_photo)
        logo_label.image = logo_photo
        logo_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Button for reading text from camera
        camera_button = ttk.Button(self, text="Read Text from Camera", command=read_text_from_camera)
        camera_button.grid(row=1, column=0, padx=10, pady=10)

        # Button for object detection
        object_detection_button = ttk.Button(self, text="Object Detection",
                                             command=lambda: object_detection(self.model))
        object_detection_button.grid(row=1, column=1, padx=10, pady=10)


# Start the application
if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
