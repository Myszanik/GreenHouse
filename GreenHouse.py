import tkinter as tk
from threading import Thread
#from datetime import datetime
import time
from PIL import Image, ImageTk  # Make sure to install Pillow library
from tkinter import messagebox

# Crop data with ideal conditions, planting start month, and harvesting month
crop_data = {
   'Tomato': {
       'ideal_temperature': (20, 30),  # Celsius
       'ideal_humidity': (50, 70),  # Percentage
       'ideal_soil_moisture': (75, 85),  # Percentage
       'ideal_light': (350, 1000),  # Lux
       'temperature_schedule': [
           (1, 13), (2, 14.3), (3, 15.6), (4, 16.9), (5, 18.2),
           (6, 19.5), (7, 21), (8, 22.5), (9, 24), (10, 26),
           (11, 28), (12, 30), (13, 32.7), (14, 35.4), (15, 32.7),
           (16, 30), (17, 28), (18, 26), (19, 24), (20, 22.5),
           (21, 21), (22, 19.5), (23, 18.2), (0, 15.6)
       ],
       'humidity_schedule': [
           (1, 85), (2, 87), (3, 88), (4, 89), (5, 90),
           (6, 90), (7, 88), (8, 85), (9, 80), (10, 75),
           (11, 70), (12, 65), (13, 60), (14, 55), (15, 60),
           (16, 65), (17, 70), (18, 75), (19, 77), (20, 79),
           (21, 81), (22, 83), (23, 85), (0, 86)
       ],
       'soil_moisture_schedule': [
           (1, 80), (2, 82), (3, 84), (4, 85), (5, 86),
           (6, 87), (7, 85), (8, 83), (9, 80), (10, 78),
           (11, 75), (12, 73), (13, 70), (14, 68), (15, 70),
           (16, 73), (17, 75), (18, 77), (19, 79), (20, 81),
           (21, 83), (22, 85), (23, 83), (0, 85)
       ],
       'light_schedule': [
           (1, 0), (2, 50), (3, 100), (4, 150), (5, 200),
           (6, 250), (7, 350), (8, 500), (9, 650), (10, 800),
           (11, 950), (12, 1100), (13, 1150), (14, 1200), (15, 1150),
           (16, 1100), (17, 950), (18, 800), (19, 650), (20, 500),
           (21, 350), (22, 200), (23, 150), (0, 100)
       ],
       'heater_on_threshold': 20,
       'heater_off_threshold': 25,
       'fan_on_threshold': 30,
       'fan_off_threshold': 25,
       'irrigation_on_threshold': 75,
       'irrigation_off_threshold': 75,
       'light_on_threshold': 349,
       'light_off_threshold': 351
   },
   'Cucumber': {
       'ideal_temperature': (18, 27),  # Celsius
       'ideal_humidity': (60, 80),  # Percentage
       'ideal_soil_moisture': (70, 85),  # Percentage
       'ideal_light': (350, 1000),  # Lux
       'temperature_schedule': [
           (1, 13), (2, 14.3), (3, 15.6), (4, 16.9), (5, 18.2),
           (6, 19.5), (7, 21), (8, 22.5), (9, 24), (10, 26),
           (11, 28), (12, 30), (13, 32.7), (14, 35.4), (15, 32.7),
           (16, 30), (17, 28), (18, 26), (19, 24), (20, 22.5),
           (21, 21), (22, 19.5), (23, 18.2), (0, 15.6)
       ],
       'humidity_schedule': [
           (1, 85), (2, 87), (3, 88), (4, 89), (5, 90),
           (6, 90), (7, 88), (8, 85), (9, 80), (10, 75),
           (11, 70), (12, 65), (13, 60), (14, 55), (15, 60),
           (16, 65), (17, 70), (18, 75), (19, 77), (20, 79),
           (21, 81), (22, 83), (23, 85), (0, 86)
       ],
       'soil_moisture_schedule': [
           (1, 80), (2, 82), (3, 84), (4, 85), (5, 86),
           (6, 87), (7, 84), (8, 82), (9, 78), (10, 75),
           (11, 72), (12, 69), (13, 67), (14, 65), (15, 68),
           (16, 71), (17, 74), (18, 77), (19, 79), (20, 81),
           (21, 83), (22, 85), (23, 83), (0, 85)
       ],
       'light_schedule': [
           (1, 0), (2, 50), (3, 100), (4, 150), (5, 200),
           (6, 250), (7, 350), (8, 500), (9, 650), (10, 800),
           (11, 950), (12, 1100), (13, 1150), (14, 1200), (15, 1150),
           (16, 1100), (17, 950), (18, 800), (19, 650), (20, 500),
           (21, 350), (22, 200), (23, 150), (0, 100)
       ],
       'heater_on_threshold': 18,
       'heater_off_threshold': 22,
       'fan_on_threshold': 27,
       'fan_off_threshold': 24,
       'irrigation_on_threshold': 70,
       'irrigation_off_threshold': 70,
       'light_on_threshold': 349,
       'light_off_threshold': 351
   },
    'Strawberry': {
       'ideal_temperature': (15, 25),  # Celsius
       'ideal_humidity': (60, 80),  # Percentage
       'ideal_soil_moisture': (70, 80),  # Percentage
       'ideal_light': (200, 800),  # Lux
       'planting_start': 'April',
       'harvesting_month': 'June',
       'temperature_schedule': [
           (1, 12), (2, 13.5), (3, 15), (4, 16.5), (5, 18),
           (6, 19.5), (7, 21), (8, 22.5), (9, 24), (10, 25),
           (11, 24), (12, 23), (13, 22), (14, 21), (15, 20),
           (16, 19), (17, 18), (18, 17), (19, 16), (20, 15),
           (21, 14), (22, 13), (23, 12), (0, 11)
       ],
       'humidity_schedule': [
           (1, 70), (2, 72), (3, 74), (4, 75), (5, 76),
           (6, 77), (7, 78), (8, 79), (9, 80), (10, 78),
           (11, 76), (12, 74), (13, 72), (14, 70), (15, 68),
           (16, 66), (17, 64), (18, 62), (19, 60), (20, 62),
           (21, 64), (22, 66), (23, 68), (0, 70)
       ],
       'soil_moisture_schedule': [
           (1, 72), (2, 74), (3, 76), (4, 78), (5, 80),
           (6, 79), (7, 78), (8, 77), (9, 76), (10, 75),
           (11, 74), (12, 73), (13, 72), (14, 71), (15, 70),
           (16, 69), (17, 68), (18, 67), (19, 66), (20, 67),
           (21, 68), (22, 69), (23, 70), (0, 72)
       ],
       'light_schedule': [
           (1, 0), (2, 30), (3, 60), (4, 90), (5, 120),
           (6, 150), (7, 200), (8, 300), (9, 400), (10, 500),
           (11, 600), (12, 700), (13, 750), (14, 800), (15, 750),
           (16, 700), (17, 600), (18, 500), (19, 400), (20, 300),
           (21, 200), (22, 150), (23, 100), (0, 50)
       ],
       'heater_on_threshold': 15,
       'heater_off_threshold': 20,
       'fan_on_threshold': 25,
       'fan_off_threshold': 20,
       'irrigation_on_threshold': 70,
       'irrigation_off_threshold': 75,
       'light_on_threshold': 199,
       'light_off_threshold': 201
   },
}


# Define time schedule for simulation
time_per_hour = 1  # Seconds in simulation for one hour
sunrise_hour = 8
sunset_hour = 18

tomato_images = [
    "/Users/dom/Desktop/Vegetables/Tomato/stage0-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage1-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage2-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage3-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage4-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage5-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage6-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Tomato/stage7-removebg-preview.png"
]

cucumber_images = [
    "/Users/dom/Desktop/Vegetables/Cucumber/stage0-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage1-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage2-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage3-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage4-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage5-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage6-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Cucumber/stage7-removebg-preview.png"
]

strawberry_images = [
    "/Users/dom/Desktop/Vegetables/Strawberry/stage0-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage1-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage2-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage3-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage4-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage5-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage5-removebg-preview.png",
    "/Users/dom/Desktop/Vegetables/Strawberry/stage6-removebg-preview.png"
]


def load_image(image_path):
    return Image.open(image_path)

def update_tomato_image(day):
    stage = day // 2  # Show image every 2 days
    if stage >= len(tomato_images):
        stage = len(tomato_images) - 1  # Show last image if exceeding the range
    img = load_image(tomato_images[stage])
    img = img.resize((300, 300))  # Resize image to fit the label
    img = ImageTk.PhotoImage(img)
    tomato_image_label.config(image=img)
    tomato_image_label.image = img

def update_cucumber_image(day):
    stage = day // 2  # Show image every 2 days
    if stage >= len(cucumber_images):
        stage = len(cucumber_images) - 1  # Show last image if exceeding the range
    img = load_image(cucumber_images[stage])
    img = img.resize((300, 300))  # Resize image to fit the label
    img = ImageTk.PhotoImage(img)
    cucumber_image_label.config(image=img)
    cucumber_image_label.image = img

def update_strawberry_image(day):
    stage = day // 2  # Show image every 2 days
    if stage >= len(strawberry_images):
        stage = len(strawberry_images) - 1  # Show last image if exceeding the range
    img = load_image(strawberry_images[stage])
    img = img.resize((300, 300))  # Resize image to fit the label
    img = ImageTk.PhotoImage(img)
    strawberry_image_label.config(image=img)
    strawberry_image_label.image = img

# Function to generate sensor data based on the selected crop and time of day
def generate_sensor_data(crop_info, current_hour):
   temperature_schedule = crop_info['temperature_schedule']
   humidity_schedule = crop_info['humidity_schedule']
   soil_moisture_schedule = crop_info['soil_moisture_schedule']
   light_schedule = crop_info['light_schedule']


   temperature = next(temp for h, temp in temperature_schedule if h == current_hour)
   humidity = next(hum for h, hum in humidity_schedule if h == current_hour)
   soil_moisture = next(moisture for h, moisture in soil_moisture_schedule if h == current_hour)
   light = next(lux for h, lux in light_schedule if h == current_hour)


   return {
       'temperature': temperature,
       'humidity': humidity,
       'soil_moisture': soil_moisture,
       'light': light,
   }


# Function to simulate control logic
def control_system(data, crop_info):
   fan_status = 'OFF'
   heater_status = 'OFF'
   irrigation_status = 'OFF'
   light_status = 'OFF'


   # Control heater based on temperature
   if data['temperature'] < crop_info['heater_on_threshold']:
       heater_status = 'ON'
   elif data['temperature'] > crop_info['heater_off_threshold']:
       heater_status = 'OFF'


   # Control fan based on temperature
   if data['temperature'] > crop_info['fan_on_threshold']:
       fan_status = 'ON'
   elif data['temperature'] < crop_info['fan_off_threshold']:
       fan_status = 'OFF'


   # Control irrigation based on soil moisture
   if data['soil_moisture'] < crop_info['irrigation_on_threshold']:
       irrigation_status = 'ON'
   elif data['soil_moisture'] > crop_info['irrigation_off_threshold']:
       irrigation_status = 'OFF'


   # Control lights based on soil moisture
   if data['light'] < crop_info['light_on_threshold']:
       light_status = 'ON'
   elif data['light'] > crop_info['light_off_threshold']:
       light_status = 'OFF'


   return fan_status, heater_status, irrigation_status, light_status


# Function to update data periodically
def update_data_periodically(crop_info):
    global simulation_day, simulation_hour, current_day_period, simulation_running

    # Initialize simulation variables
    simulation_day = 0
    simulation_hour = sunrise_hour
    current_day_period = 'Morning'

    water_level = 100
    refill_status = 'OFF'

    while True:  # Run the simulation indefinitely
        current_hour = simulation_hour

        # Generate sensor data
        sensor_data = generate_sensor_data(crop_info, current_hour)

        fan_status, heater_status, irrigation_status, light_status = control_system(sensor_data, crop_info)

        # Update UI with sensor data
        temp_label.config(
            text=f"Temperature: {sensor_data['temperature']}°C ({crop_info['ideal_temperature'][0]}-{crop_info['ideal_temperature'][1]})")
        hum_label.config(
            text=f"Humidity: {sensor_data['humidity']}% ({crop_info['ideal_humidity'][0]}-{crop_info['ideal_humidity'][1]})")
        soil_label.config(
            text=f"Soil Moisture: {sensor_data['soil_moisture']}% ({crop_info['ideal_soil_moisture'][0]}-{crop_info['ideal_soil_moisture'][1]})")
        light_label.config(
            text=f"Light: {sensor_data['light']} Lux ({crop_info['ideal_light'][0]}-{crop_info['ideal_light'][1]})")

        # Update water level and refill status
        if irrigation_status == 'ON' and water_level > 0:
            water_level -= 5
            if water_level < 0:
                water_level = 0  # Ensure water level does not go below 0

        if water_level < 10:
            refill_status = 'ON'
            refill_label.config(text="Refilling water tank...", bg='#1ea0b3', fg='black')
            refill_icon.itemconfig("icon", fill="#003300")

            while water_level < 100:
                water_level += 10
                if water_level > 100:
                    water_level = 100  # Cap the water level at 100%
                water_level_label.config(
                    text=f"Tank Water Level: {water_level}% ({get_water_status(water_level)})")
                # Update the water level bar
                water_level_canvas.coords(water_level_bar2, 0, 100 - water_level, 30, 100)
                root.update()  # Update the UI
                time.sleep(1)

            refill_label.config(text="Water Refill: OFF", bg='#1ea0b3', bd=4, fg='black')
            refill_status = 'OFF'
            refill_icon.itemconfig("icon", fill="red")

        else:
            water_level_label.config(
                text=f"Tank Water Level: {water_level}% ({get_water_status(water_level)})")
            water_level_canvas.coords(water_level_bar2, 0, 100 - water_level, 30, 100)

        # Update system status
        update_system_status(fan_status, fan_label, fan_icon, '#003300', 'red')
        update_system_status(heater_status, heater_label, heater_icon, '#003300', 'red')
        update_system_status(irrigation_status, irrigation_label, irrigation_icon, '#003300', 'red')
        update_system_status(light_status, lights_label, light_icon, '#003300', 'red')

        # Update labels
        simulation_time_label.config(text=f"Simulation Time: Day {simulation_day}, {simulation_hour}:00")
        day_period_label.config(text=f"Part of Day: {current_day_period}")

        # Update tomato image every 2 days
        if crop_info == crop_data['Cucumber']:
            update_cucumber_image(simulation_day)
        elif crop_info == crop_data['Strawberry']:
            update_strawberry_image(simulation_day)
        else:
            update_tomato_image(simulation_day)

        # Check if it's time to show the "Ready to Harvest" button
        if simulation_day == 15 and simulation_hour == 10:
            start_button.grid_forget()
            harvest_button.grid(row=10, columnspan=18, pady=10)  # Show the button in the main thread
            break

        # Move to the next simulated hour
        simulation_hour += 1
        if simulation_hour >= 24:
            simulation_hour = 0
            simulation_day += 1  # Increment the day count

        # Determine the part of the day
        if 4 <= simulation_hour < 12:
            current_day_period = 'Morning'
        elif 12 <= simulation_hour < 17:
            current_day_period = 'Afternoon'
        elif 17 <= simulation_hour < 21:
            current_day_period = 'Evening'
        else:
            current_day_period = 'Night'

        root.update_idletasks()  # Ensures UI updates are processed
        time.sleep(time_per_hour)


# Function to get water status based on water level
def get_water_status(water_level):
   if water_level > 80:
       return "Full"
   elif 30 <= water_level <= 80:
       return "Normal"
   else:
       return "Low"

# Function to update system status
def update_system_status(status, label, icon, on_color, off_color):
   if status == 'ON':
       label.config(text=f"{label.cget('text').split(':')[0]}: ON", fg='black')
       icon.itemconfig("icon", fill=on_color)
   else:
       label.config(text=f"{label.cget('text').split(':')[0]}: OFF", fg='black')
       icon.itemconfig("icon", fill=off_color)

# Function to start the simulation
def start_simulation():
    selected_crop = crop_selection.get()
    if selected_crop:
        crop_info = crop_data[selected_crop]
        if selected_crop == 'Tomato':
            Thread(target=update_data_periodically, args=(crop_info,), daemon=True).start()
        elif selected_crop == 'Cucumber':
            Thread(target=update_data_periodically, args=(crop_info,), daemon=True).start()
            update_cucumber_image(simulation_day)  # Ensure this updates based on the day of simulation
        elif selected_crop == 'Strawberry':
            Thread(target=update_data_periodically, args=(crop_info,), daemon=True).start()
            update_strawberry_image(simulation_day)

# Initialize Tkinter root
root = tk.Tk()
root.title("Smart Greenhouse System")
root.config(bg='#1ea0b3')


# Set the window size
root.geometry("1150x1000")


# Create and place sensor data labels
# Configure the main window grid
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Create a frame to hold the sensor labels with a border
border_thickness = 5  # Change this value to adjust the border thickness
sensor_frame = tk.Frame(root, borderwidth=border_thickness, bd=border_thickness, relief="groove", bg='#1ea0b3', highlightbackground="black", highlightthickness=border_thickness)
sensor_frame.grid(row=0, column=4, rowspan=4, padx=0, pady=10, sticky='nsew')

# Make sure the frame does not resize itself based on its contents
sensor_frame.grid_propagate(False)

# Create and place the labels inside the frame
temp_label = tk.Label(sensor_frame, text="Temperature: ", width=25, bg='#1ea0b3', font=('Helvetica', 20), fg='black')
temp_label.grid(row=0, column=0, pady=5)

hum_label = tk.Label(sensor_frame, text="Humidity: ", width=25, bg='#1ea0b3', font=('Helvetica', 20), fg='black')
hum_label.grid(row=1, column=0, pady=5)

soil_label = tk.Label(sensor_frame, text="Soil Moisture: ", width=25, bg='#1ea0b3', font=('Helvetica', 20), fg='black')
soil_label.grid(row=2, column=0, pady=5)

light_label = tk.Label(sensor_frame, text="Light: ", width=25, bg='#1ea0b3', font=('Helvetica', 20), fg='black')
light_label.grid(row=3, column=0, pady=5)

# Adjust row and column weights for the root grid to make sure the frame expands if the window is resized
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(1, weight=1)

# Configure the frame's grid to expand and fill space
sensor_frame.grid_rowconfigure(0, weight=1)
sensor_frame.grid_rowconfigure(1, weight=1)
sensor_frame.grid_rowconfigure(2, weight=1)
sensor_frame.grid_rowconfigure(3, weight=1)
sensor_frame.grid_columnconfigure(0, weight=1)


# Create water level indicator
# Configure the main window grid
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)

# Create a frame to hold the water labels with a border
border_thickness = 5  # Change this value to adjust the border thickness
water_frame = tk.Frame(root, borderwidth=border_thickness, bd=border_thickness, relief="groove", bg='#1ea0b3', highlightbackground="black", highlightthickness=border_thickness)
water_frame.grid(row=5, column=4, rowspan=4, padx=0, pady=0, sticky='nsew')

# Make sure the frame does not resize itself based on its contents
water_frame.grid_propagate(False)

water_level_label = tk.Label(root, text="Tank Water Level: ", width=27, font=('Verdana', 18), fg='black', bg='#1ea0b3')
water_level_label.grid(row=5, column=4, pady=15)
water_level_canvas = tk.Canvas(root, width=30, height=100, bg='white')
water_level_canvas.grid(row=6, column=4)
water_level_bar = water_level_canvas.create_rectangle(0, 100, 30, 100, fill="white")
water_level_bar2 = water_level_canvas.create_rectangle(0, 100, 30, 0, fill="blue")


# Create refill status label with border
refill_label = tk.Label(root, text="Water Refill: OFF", width=20, font=('Helvetica', 20, 'bold'), bd=4, relief='solid', bg='#1ea0b3', fg='black')
refill_label.grid(row=7, column=4, padx=10, pady=0)  # Added padding for spacing
refill_icon = tk.Canvas(root, width=30, height=30, bg='#e0f7fa', bd=2, relief='solid')
refill_icon.grid(row=8, column=4, pady=15)
refill_icon.create_oval(5, 5, 34, 34, fill="red", tags="icon")

# Adjust row and column weights for the root grid to make sure the frame expands if the window is resized
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(4, weight=1)

# Configure the frame's grid to expand and fill space
water_frame.grid_rowconfigure(0, weight=1)
water_frame.grid_rowconfigure(1, weight=1)
water_frame.grid_rowconfigure(2, weight=1)
water_frame.grid_rowconfigure(3, weight=1)
water_frame.grid_columnconfigure(0, weight=1)


# Create frames for control systems with labels and icons
def create_system_frame(system_name, row, col, bg_color):
    # Create a frame for the system control with a border color
    outer_frame = tk.Frame(root, bd=2, bg=colors[system_name], relief='solid')  # This is the outer frame with the border color

    # Create a colored inner frame for the system control background
    inner_frame = tk.Frame(outer_frame, bd=2, bg=colors[system_name])
    inner_frame.pack(padx=5, pady=5, fill='both', expand=True)  # Adding padding inside the border

    # Create labels for system status
    status_label = tk.Label(inner_frame, text=f"{system_name}: OFF", font=('Helvetica', 20, 'bold'), width=25, bg=colors[system_name], fg='black', bd=3, relief='solid')
    status_label.grid(row=0, column=0, pady=10)

    # Create icon canvas
    icon_canvas = tk.Canvas(inner_frame, width=30, height=30, bg='#e0f7fa', bd=2, relief='solid')
    icon_canvas.grid(row=0, column=1)
    icon_canvas.create_oval(5, 5, 34, 34, fill="red", tags="icon")

    # Place the outer frame in the grid
    outer_frame.grid(row=row, column=col)

    return status_label, icon_canvas


# Define colors for each system
colors = {
    "Fan": '#ff7043',          # Coral Orange
    "Heater": '#00796b',       # Deep Teal
    "Irrigation": '#ffca28',   # Bright Yellow
    "Light": '#8e24aa'         # Purple
}

fan_label, fan_icon = create_system_frame("Fan", 0, 0, colors["Fan"])
heater_label, heater_icon = create_system_frame("Heater", 1, 0, colors["Heater"])
irrigation_label, irrigation_icon = create_system_frame("Irrigation", 2, 0, colors["Irrigation"])
lights_label, light_icon = create_system_frame("Light", 3, 0, colors["Light"])


# Create crop selection dropdown menu
crop_selection = tk.StringVar()
crop_selection.set("Select Crop")

# Initialize confirmation message as an empty string
confirmation_message = tk.StringVar()
confirmation_message.set("")  # This hides the confirmation message initially

# Function to handle crop selection
def select_crop():
    selected_crop = crop_selection.get()
    if selected_crop == "Select Crop":
        # Inform the user that they need to select a crop
        messagebox.showwarning("Selection Error", "Please select a crop first.")
    else:
        # Display a confirmation message in the label
        confirmation_message.set(f"Selected Crop: {selected_crop}")
        start_button.config(state=tk.NORMAL)  # Enable the Start Simulation button

        # Hide the confirmation message after 3 seconds (3000 milliseconds)
        root.after(1500, hide_message)


def hide_message():
    confirmation_message.set("")  # Clear the confirmation message

#Configure the main window grid
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(9, weight=1)  # Ensure column 9 can expand

# Create a frame to hold the sensor labels with a border
border_thickness = 5  # Change this value to adjust the border thickness
crop_frame = tk.Frame(root, borderwidth=border_thickness, bd=border_thickness, relief="groove", bg='#1ea0b3', highlightbackground="black", highlightthickness=border_thickness)
crop_frame.grid(row=0, column=9, rowspan=4, padx=10, pady=10, sticky='nsew')

# Make sure the frame does not resize itself based on its contents
sensor_frame.grid_propagate(False)

# Create an OptionMenu with a colored border
crop_menu = tk.OptionMenu(root, crop_selection, *crop_data.keys())
crop_menu.config(bd=0, font=('Verdana', 18), width=20, height=0, highlightbackground="#1ea0b3", highlightcolor="#1ea0b3", highlightthickness=0)
crop_menu.grid(row=0, column=9, padx=5, pady=5)

# Button to confirm crop selection
select_crop_button = tk.Button(root, text="Select Crop", font=('Verdana', 18), width=18, command=select_crop, fg='black', bg='#1ea0b3', bd=5, highlightbackground="#1ea0b3", highlightcolor="#1ea0b3", highlightthickness=5)
select_crop_button.grid(row=1, column=9, pady=5)

# Simulation time and part of day labels
simulation_time_label = tk.Label(root, text="Simulation Time: ", width=25, font=('Verdana', 18), fg='black', bg='#1ea0b3')
simulation_time_label.grid(row=2, column=9)
day_period_label = tk.Label(root, text="Part of Day: ", width=25, font=('Verdana', 18), fg='black', bg='#1ea0b3')
day_period_label.grid(row=3, column=9)

# Adjust row and column weights for the root grid to make sure the frame expands if the window is resized
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=0)
root.grid_rowconfigure(3, weight=0)
root.grid_columnconfigure(4, weight=1)

# Configure the frame's grid to expand and fill space
crop_frame.grid_rowconfigure(0, weight=1)
crop_frame.grid_rowconfigure(1, weight=1)
crop_frame.grid_rowconfigure(2, weight=1)
crop_frame.grid_rowconfigure(3, weight=1)
crop_frame.grid_columnconfigure(0, weight=1)


# Label to display crop selection confirmation, placed at row 4, column 4
confirmation_message = tk.StringVar()
confirmation_label = tk.Label(root, textvariable=confirmation_message, font=('Roboto Condensed', 23, 'bold'), bg='#1ea0b3', fg='green')
confirmation_label.grid(row=4, column=9, padx=5, pady=5)

simulation_start_message = tk.StringVar()
simulation_start_message.set("")  # This hides the simulation start message initially

simulation_start_label = tk.Label(root, textvariable=simulation_start_message, font=('Roboto Condensed', 23, 'bold'), bg='#1ea0b3', fg='green')
simulation_start_label.grid(row=4, column=4, padx=10, pady=10)
# Create a Start button for simulation with functionality
def start_simulation():
    selected_crop = crop_selection.get()
    if selected_crop:
        crop_info = crop_data[selected_crop]
        Thread(target=update_data_periodically, args=(crop_info,), daemon=True).start()

        # Display a confirmation message
        simulation_start_message.set("Simulation Started")

        # Hide the confirmation message after 3 seconds (3000 milliseconds)
        root.after(1500, hide_simulation_start_message)


def hide_simulation_start_message():
    simulation_start_message.set("")  # Clear the simulation start message

# Step 1: Create a StringVar for the harvest message
harvest_message = tk.StringVar()
harvest_message.set("")  # Initially, hide the harvest message

# Step 2: Create a Label to display the harvest message
harvest_label = tk.Label(root, textvariable=harvest_message, font=('Roboto Condensed', 23, 'bold'), bg='#1ea0b3', fg='green')
harvest_label.grid(row=4, column=0, padx=10, pady=10)  # Adjust row and column as needed

def harvest():
    # Show a message indicating successful harvest
    selected_crop = crop_selection.get()
    if selected_crop:
        message = f"Well Done! {selected_crop} harvested."
        harvest_message.set(message)  # Assuming you have a StringVar for displaying messages
        root.after(2500, clear_harvest_message)  # Clear the message after 3 seconds
        harvest_button.grid_forget()  # Hide the harvest button
        start_button.grid(row=10, columnspan=18, pady=10)  # Show the start button
        root.update_idletasks()


# Perform any additional UI updates or resets here
def clear_harvest_message():
    harvest_message.set("")  # Clear the harvest message

# Start simulation button
start_button = tk.Button(root, text="Start Simulation", justify='center', width=40, font=('Arial', 26), command=start_simulation, fg='black', bg='#1ea0b3')
start_button.grid(row=10, columnspan=18, pady=10)

# Harvest button (initially hidden)
harvest_button = tk.Button(root, text="Ready to Harvest", justify='center', width=40, font=('Arial', 26), command=harvest, fg='black', bg='#1ea0b3')
start_button.grid(row=10, columnspan=18, pady=10)

tomato_image_label = tk.Label(root, bg='#1ea0b3')
tomato_image_label.grid(row=12, column=4, rowspan=6)

cucumber_image_label = tk.Label(root, bg='#1ea0b3')
cucumber_image_label.grid(row=12, column=4, rowspan=6)

strawberry_image_label = tk.Label(root, bg='#1ea0b3')
strawberry_image_label.grid(row=12, column=4, rowspan=6)

# Start the Tkinter main loop
root.mainloop()

