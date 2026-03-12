import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr  # Importing speech recognition library

class Cab:
    def __init__(self, cab_type, base_fare, rate_per_km):
        self.cab_type = cab_type
        self.base_fare = base_fare
        self.rate_per_km = rate_per_km

    def calculate_fare(self, distance):
        return self.base_fare + (self.rate_per_km * distance)


class CabBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Cab Booking System")

        # Set background color for the root window
        self.root.configure(bg="lightblue")

        # List of available cabs
        self.cabs = [
            Cab("Standard", 50, 10),  # base fare 50, rate per km 10
            Cab("Luxury", 100, 15),   # base fare 100, rate per km 15
            Cab("SUV", 150, 20)       # base fare 150, rate per km 20
        ]
        
        # Label
        self.label = tk.Label(root,text=" ONLINE CAB PRICE CALCULATOR  ", font=("Arial", 20), bg="lightblue")
        self.label.pack(pady=40)
        
        # Cab selection dropdown
        self.cab_label = tk.Label(root, text="Select Cab Type:", font=("Arial", 16), bg="lightblue")
        self.cab_label.pack(pady=20)
        
        self.cab_type_var = tk.StringVar(root)
        self.cab_type_var.set(self.cabs[0].cab_type)  # Set default value
        self.cab_menu = tk.OptionMenu(root, self.cab_type_var, *[cab.cab_type for cab in self.cabs])
        self.cab_menu.pack(pady=20)

        # Distance input
        self.distance_label = tk.Label(root, text="Enter Distance (in km):", font=("Arial", 16), bg="lightblue")
        self.distance_label.pack(pady=20)

        self.distance_entry = tk.Entry(root, font=("Arial", 16))
        self.distance_entry.pack(pady=20)

        # Book Button
        self.book_button = tk.Button(root, text="Book Cab", font=("Arial", 16), command=self.book_cab, bg="lightgreen")
        self.book_button.pack(pady=20)

        # Exit Button
        self.exit_button = tk.Button(root, text="Exit", font=("Arial", 12), command=root.quit, bg="lightcoral")
        self.exit_button.pack(pady=20)

        # Speech Recognition Button
        self.speech_button = tk.Button(root, text="Speak to Book Cab", font=("Arial", 14), command=self.listen_for_speech, bg="lightyellow")
        self.speech_button.pack(pady=20)

    def book_cab(self):
        try:
            # Get selected cab type and distance
            selected_cab_type = self.cab_type_var.get()
            distance = float(self.distance_entry.get())
            
            # Find the selected cab
            selected_cab = next(cab for cab in self.cabs if cab.cab_type == selected_cab_type)
            
            # Calculate fare
            fare = selected_cab.calculate_fare(distance)
            
            # Show the result in a message box
            messagebox.showinfo("Booking Confirmation", 
                                f"You have selected the {selected_cab.cab_type} cab.\n"
                                f"Distance: {distance} km\n"
                                f"Total fare: RS : {fare:.2f}")
        
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for distance.")

    def listen_for_speech(self):
        # Initialize recognizer class (for recognizing the speech)
        recognizer = sr.Recognizer()

        # Use the default microphone as the audio source
        with sr.Microphone() as source:
            messagebox.showinfo("Listening", "Please speak the cab type and distance.")
            recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
            audio = recognizer.listen(source)  # Listen for the first phrase

            try:
                # Recognize speech using Google Speech Recognition
                speech_text = recognizer.recognize_google(audio)
                messagebox.showinfo("Speech Recognized", f"You said: {speech_text}")
                self.process_speech_input(speech_text)

            except sr.UnknownValueError:
                messagebox.showerror("Speech Recognition", "Sorry, I could not understand your speech.")
            except sr.RequestError:
                messagebox.showerror("Speech Recognition", "Could not request results; check your network connection.")

    def process_speech_input(self, speech_text):
        try:
            # Extract cab type and distance from the recognized speech
            # Assuming the format: "Book a [cab type] for [distance] kilometers"
            speech_text = speech_text.lower()

            cab_type = None
            for cab in self.cabs:
                if cab.cab_type.lower() in speech_text:
                    cab_type = cab
                    break

            # Find the distance in the speech
            distance = None
            words = speech_text.split()
            for word in words:
                if word.isdigit():
                    distance = float(word)
                    break

            if cab_type and distance:
                self.cab_type_var.set(cab_type.cab_type)
                self.distance_entry.delete(0, tk.END)
                self.distance_entry.insert(0, str(distance))
                self.book_cab()
            else:
                messagebox.showerror("Speech Processing Error", "Could not extract valid cab type or distance from speech.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing your speech: {str(e)}")

# Create main window
root = tk.Tk()
app = CabBookingApp(root)
root.mainloop()