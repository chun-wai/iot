import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import time

# Global variables for GUI
resistance_var = None
incline_var = None
speed_var = None
distance_var = None
power_var = None  # Declare power_var as a global variable
countdown_var = None  # Declare countdown_var as a global variable

# Global variables for simulation
training_active = False
countdown_active = False
start_time = 0
distance_traveled = 0

def calculate_power(speed, resistance):
    # Calculate power using the formula: Power = Speed * Resistance
    power = speed * resistance
    return power

def update_values():
    global start_time, distance_traveled

    if training_active:
        # Get the current time
        current_time = time.time()

        # Calculate elapsed time since the user started pedaling
        elapsed_time = current_time - start_time

        # Simulate speed based on resistance and incline levels (replace with actual logic)
        resistance = int(resistance_var.get())
        incline = int(incline_var.get())
        speed = resistance + incline  # This is just a simple example, adjust as needed

        # Calculate distance traveled based on speed and elapsed time
        distance_traveled = speed * elapsed_time / 3600  # Convert seconds to hours

        # Calculate power using speed and resistance
        power = calculate_power(speed, resistance)

        # Update GUI with calculated values
        speed_var.set(f"{speed} km/h")
        distance_var.set(f"{distance_traveled:.2f} km")
        power_var.set(f"{power:.2f} Watts")  # Update power value

    # Schedule the next update after a delay (in milliseconds)
    root.after(1000, update_values)

def on_resistance_change(event):
    # Update resistance value from user input
    try:
        resistance = int(resistance_entry.get())
        if 0 <= resistance <= 10:
            resistance_var.set(resistance)
        else:
            raise ValueError
    except ValueError:
        resistance_entry.delete(0, tk.END)
        resistance_var.set("Invalid Input")

def on_incline_change(event):
    # Update incline value from user input
    try:
        incline = int(incline_entry.get())
        if 0 <= incline <= 10:
            incline_var.set(incline)
        else:
            raise ValueError
    except ValueError:
        incline_entry.delete(0, tk.END)
        incline_var.set("Invalid Input")

def start_training():
    global training_active, countdown_active, start_time, distance_traveled
    if not training_active:
        training_active = True
        countdown_active = True
        start_time = time.time()  # Record the start time of pedaling
        distance_traveled = 0  # Reset distance traveled
        countdown_timer()
        update_values()

def stop_training():
    global training_active, countdown_active, start_time, distance_traveled
    if training_active:
        training_active = False
        countdown_active = False
        start_time = 0  # Reset the start time
        distance_traveled = 0  # Reset distance traveled
        speed_var.set("0 km/h")  # Reset speed display
        distance_var.set("0.00 km")  # Reset distance display
        countdown_var.set("5:00")  # Reset the countdown display

def countdown_timer():
    global countdown_active
    if countdown_active:
        remaining_time = 300 - int(time.time() - start_time)
        if remaining_time <= 0:
            stop_training()
            return
        countdown_var.set(f"{remaining_time // 60}:{remaining_time % 60:02}")
        root.after(1000, countdown_timer)
    else:
        countdown_var.set("5:00")  # Reset the countdown display


def main():
    global root, resistance_var, incline_var, speed_var, distance_var, power_var, countdown_var
    
    root = tk.Tk()
    root.title("Smart Indoor Bike Dashboard")

    # Background Image
    bg_image = Image.open("cycling_path.jpg")
    # bg_image = bg_image.resize((800, 600), Image.ANTIALIAS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0)

    # Resistance Label and Entry
    resistance_label = tk.Label(root, text="Resistance:", font=("Helvetica", 16))
    resistance_label.place(x=30, y=30)
    resistance_var = tk.StringVar()
    resistance_var.set(5)  # Default value for resistance
    resistance_entry = ttk.Entry(root, textvariable=resistance_var, font=("Helvetica", 16))
    resistance_entry.place(x=170, y=30)
    resistance_entry.bind("<Return>", on_resistance_change)

    # Incline Label and Entry
    incline_label = tk.Label(root, text="Incline:", font=("Helvetica", 16))
    incline_label.place(x=30, y=70)
    incline_var = tk.StringVar()
    incline_var.set(5)  # Default value for incline
    incline_entry = ttk.Entry(root, textvariable=incline_var, font=("Helvetica", 16))
    incline_entry.place(x=170, y=70)
    incline_entry.bind("<Return>", on_incline_change)

    # Power Label
    power_label = tk.Label(root, text="Power:", font=("Helvetica", 16))
    power_label.place(x=30, y=200)
    power_var = tk.StringVar()
    power_value_label = tk.Label(root, textvariable=power_var, font=("Helvetica", 16))
    power_value_label.place(x=170, y=200)

    root.after(1000, update_values)  # Start the update loop

    # Speed Label
    speed_label = tk.Label(root, text="Speed:", font=("Helvetica", 16))
    speed_label.place(x=30, y=120)
    speed_var = tk.StringVar()
    speed_value_label = tk.Label(root, textvariable=speed_var, font=("Helvetica", 16))
    speed_value_label.place(x=170, y=120)

    # Distance Label
    distance_label = tk.Label(root, text="Distance:", font=("Helvetica", 16))
    distance_label.place(x=30, y=160)
    distance_var = tk.StringVar()
    distance_value_label = tk.Label(root, textvariable=distance_var, font=("Helvetica", 16))
    distance_value_label.place(x=170, y=160)

    # Countdown Label
    countdown_label = tk.Label(root, text="Countdown:", font=("Helvetica", 16))
    countdown_label.place(x=30, y=240)
    countdown_var = tk.StringVar()
    countdown_value_label = tk.Label(root, textvariable=countdown_var, font=("Helvetica", 16))
    countdown_value_label.place(x=170, y=240)
    
    # Start Button
    start_button = ttk.Button(root, text="START", command=start_training)
    start_button.place(x=50, y=300)

    # Stop Button
    stop_button = ttk.Button(root, text="STOP", command=stop_training)
    stop_button.place(x=150, y=300)

    root.mainloop()

if __name__ == "__main__":
    main()
