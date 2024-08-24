import tkinter as tk
from threading import Thread
from datetime import datetime
import time
import math

# Crop data with ideal conditions, planting start month, and harvesting month
crop_data = {
    'Tomato': {
        'ideal_temperature': (20, 30),  # Celsius
        'ideal_humidity': (50, 70),  # Percentage
        'ideal_soil_moisture': (50, 80),  # Percentage
        'ideal_light': (600, 1000),  # Lux
        'planting_start': 'March',
        'harvesting_month': 'August',
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
    'Lettuce': {
        'ideal_temperature': (15, 25),  # Celsius
        'ideal_humidity': (60, 80),  # Percentage
        'ideal_soil_moisture': (40, 70),  # Percentage
        'ideal_light': (400, 700),  # Lux
        'planting_start': 'April',
        'harvesting_month': 'September',
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
        'heater_on_threshold': 18,
        'heater_off_threshold': 22,
        'fan_on_threshold': 27,
        'fan_off_threshold': 24,
        'irrigation_on_threshold': 70,
        'irrigation_off_threshold': 70,
        'light_on_threshold': 349,
        'light_off_threshold': 351
    }
}

# Define time schedule for simulation
time_per_hour = 1  # Seconds in simulation for one hour
sunrise_hour = 6
sunset_hour = 18


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
    global simulation_day, simulation_hour, current_day_period

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
            refill_label.config(text="Refilling water...", bg='green', fg='white')
            refill_icon.itemconfig("icon", fill="green")

            while water_level < 100:
                water_level += 10
                if water_level > 100:
                    water_level = 100  # Cap the water level at 100%
                water_level_label.config(
                    text=f"Water Level: {water_level}% ({get_water_status(water_level)})")
                # Update the water level bar
                water_level_canvas.coords(water_level_bar, 0, 100 - water_level, 30, 100)
                root.update()  # Update the UI
                time.sleep(1)

            refill_label.config(text="Water Refill: OFF", bg='red')
            refill_status = 'OFF'
            refill_icon.itemconfig("icon", fill="grey")

        else:
            water_level_label.config(
                text=f"Water Level: {water_level}% ({get_water_status(water_level)})")
            water_level_canvas.coords(water_level_bar, 0, 100 - water_level, 30, 100)

        # Update system status
        update_system_status(fan_status, fan_label, fan_icon, 'green', 'red')
        update_system_status(heater_status, heater_label, heater_icon, 'green', 'red')
        update_system_status(irrigation_status, irrigation_label, irrigation_icon, 'green', 'red')
        update_system_status(light_status, lights_label, light_icon, 'green', 'red')

        # Update labels
        simulation_time_label.config(text=f"Simulation Time: Day {simulation_day}, {simulation_hour}:00")
        day_period_label.config(text=f"Part of Day: {current_day_period}")

        # Move to the next simulated hour
        simulation_hour += 1
        if simulation_hour >= 24:
            simulation_hour = 0
            simulation_day += 1  # Increment the day count

        # Determine the part of the day
        if sunrise_hour <= simulation_hour < 12:
            current_day_period = 'Morning'
        elif 12 <= simulation_hour < 18:
            current_day_period = 'Afternoon'
        else:
            current_day_period = 'Evening'

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
        label.config(text=f"{label.cget('text').split(':')[0]}: ON", bg=on_color)
        icon.itemconfig("icon", fill=on_color)
    else:
        label.config(text=f"{label.cget('text').split(':')[0]}: OFF", bg=off_color)
        icon.itemconfig("icon", fill=off_color)


# Function to handle crop selection and update UI
def select_crop():
    selected_crop = crop_selection.get()
    if selected_crop:
        crop_info = crop_data[selected_crop]
        planting_month = datetime.strptime(crop_info['planting_start'], '%B').month
        harvesting_month = datetime.strptime(crop_info['harvesting_month'], '%B').month
        current_month_label.config(text=f"Current Month: {datetime(2024, planting_month, 1).strftime('%B')}")
        planting_label.config(text=f"Planting Start Date: {crop_info['planting_start']}")
        harvesting_label.config(text=f"Harvesting Month: {crop_info['harvesting_month']}")


# Function to start the simulation
def start_simulation():
    selected_crop = crop_selection.get()
    if selected_crop:
        crop_info = crop_data[selected_crop]
        Thread(target=update_data_periodically, args=(crop_info,), daemon=True).start()


# Initialize Tkinter root
root = tk.Tk()
root.title("Smart Greenhouse System")

# Set the window size
root.geometry("1050x950")

# Create and place sensor data labels
temp_label = tk.Label(root, text="Temperature: ", font=('Helvetica', 14))
temp_label.pack(pady=5)
hum_label = tk.Label(root, text="Humidity: ", font=('Helvetica', 14))
hum_label.pack(pady=5)
soil_label = tk.Label(root, text="Soil Moisture: ", font=('Helvetica', 14))
soil_label.pack(pady=5)
light_label = tk.Label(root, text="Light: ", font=('Helvetica', 14))
light_label.pack(pady=5)

# Create water level indicator
water_level_label = tk.Label(root, text="Water Level: ", font=('Helvetica', 14))
water_level_label.pack(pady=5)
water_level_canvas = tk.Canvas(root, width=30, height=100, bg='white')
water_level_canvas.pack(pady=5)
water_level_bar = water_level_canvas.create_rectangle(0, 100, 30, 100, fill="white")
water_level_bar = water_level_canvas.create_rectangle(0, 100, 30, 0, fill="blue")

# Create refill status label and icon
refill_label = tk.Label(root, text="Water Refill: OFF", font=('Helvetica', 14, 'bold'), bg='red')
refill_label.pack(pady=5)
refill_icon = tk.Canvas(root, width=30, height=30)
refill_icon.pack()
refill_icon.create_oval(5, 5, 25, 25, fill="red", tags="icon")


# Create frames for control systems with labels and icons
def create_system_frame(system_name):
    frame = tk.Frame(root)
    label = tk.Label(frame, text=f"{system_name}: OFF", font=('Helvetica', 14, 'bold'), bg='red')
    label.pack(side=tk.LEFT, padx=10)

    icon_canvas = tk.Canvas(frame, width=30, height=30)
    icon_canvas.pack(side=tk.LEFT)
    icon_canvas.create_oval(5, 5, 25, 25, fill="red", tags="icon")

    frame.pack(pady=10, fill=tk.X)
    return label, icon_canvas


fan_label, fan_icon = create_system_frame("Fan")
heater_label, heater_icon = create_system_frame("Heater")
irrigation_label, irrigation_icon = create_system_frame("Irrigation")
lights_label, light_icon = create_system_frame("Light")

# Create crop selection dropdown menu
crop_selection = tk.StringVar()
crop_selection.set("Select Crop")
crop_menu = tk.OptionMenu(root, crop_selection, *crop_data.keys())
crop_menu.pack(pady=10)

# Button to confirm crop selection and display planting start date
select_crop_button = tk.Button(root, text="Select Crop", command=select_crop)
select_crop_button.pack(pady=5)

# Current month label
current_month_label = tk.Label(root, text="Current Month: ", font=('Helvetica', 12))
current_month_label.pack(pady=5)

# Label to show planting start date
planting_label = tk.Label(root, text="Planting Start Date: ", font=('Helvetica', 12))
planting_label.pack(pady=5)

# Label to show harvesting month
harvesting_label = tk.Label(root, text="Harvesting Month: ", font=('Helvetica', 12))
harvesting_label.pack(pady=5)

# Simulation time and part of day labels
simulation_time_label = tk.Label(root, text="Simulation Time: ", font=('Helvetica', 12))
simulation_time_label.pack(pady=5)
day_period_label = tk.Label(root, text="Part of Day: ", font=('Helvetica', 12))
day_period_label.pack(pady=5)

# Start simulation button
start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.pack(pady=20)

# Start the Tkinter main loop
root.mainloop()
