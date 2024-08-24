import tkinter as tk
from threading import Thread
from datetime import datetime
import time
from PIL import Image, ImageTk  # Make sure to install Pillow library

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
sunrise_hour = 8
sunset_hour = 18

tomato_images = [
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage0-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage1-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage2-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage3-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage4-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage5-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage6-removebg-preview.png",
    "/Users/dom/Desktop/Tomatoes/NoBackground/stage7-removebg-preview.png"
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
                water_level_canvas.coords(water_level_bar2, 0, 100 - water_level, 30, 100)
                root.update()  # Update the UI
                time.sleep(1)

            refill_label.config(text="Water Refill: OFF", bg='red')
            refill_status = 'OFF'
            refill_icon.itemconfig("icon", fill="grey")

        else:
            water_level_label.config(
                text=f"Water Level: {water_level}% ({get_water_status(water_level)})")
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
        update_tomato_image(simulation_day)

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
       label.config(text=f"{label.cget('text').split(':')[0]}: ON", bg='#26c6da', fg='black')
       icon.itemconfig("icon", fill=on_color)
   else:
       label.config(text=f"{label.cget('text').split(':')[0]}: OFF", bg='#26c6da', fg='black')
       icon.itemconfig("icon", fill=off_color)


# Function to handle crop selection and update UI
def select_crop():
   selected_crop = crop_selection.get()
   if selected_crop:
       crop_info = crop_data[selected_crop]
       #planting_month = datetime.strptime(crop_info['planting_start'], '%B').month
       #harvesting_month = datetime.strptime(crop_info['harvesting_month'], '%B').month
       #current_month_label.config(text=f"Current Month: {datetime(2024, planting_month, 1).strftime('%B')}")
       #planting_label.config(text=f"Planting Start Date: {crop_info['planting_start']}")
       #harvesting_label.config(text=f"Harvesting Month: {crop_info['harvesting_month']}")


# Function to start the simulation
def start_simulation():
   selected_crop = crop_selection.get()
   if selected_crop:
       crop_info = crop_data[selected_crop]
       Thread(target=update_data_periodically, args=(crop_info,), daemon=True).start()


# Initialize Tkinter root
root = tk.Tk()
root.title("Smart Greenhouse System")
root.config(bg='#26c6da')


# Set the window size
root.geometry("900x900")


# Create and place sensor data labels
temp_label = tk.Label(root, text="Temperature: ", width=25, bg='#26c6da', font=('Helvetica', 20), fg='black')
temp_label.grid(row=0, column=4)
hum_label = tk.Label(root, text="Humidity: ", width=25, bg='#26c6da', font=('Helvetica', 20), fg='black')
hum_label.grid(row=1, column=4)
soil_label = tk.Label(root, text="Soil Moisture: ", width=25, bg='#26c6da', font=('Helvetica', 20), fg='black')
soil_label.grid(row=2, column=4)
light_label = tk.Label(root, text="Light: ", width=25, bg='#26c6da', font=('Helvetica', 20), fg='black')
light_label.grid(row=3, column=4)


# Create water level indicator
water_level_label = tk.Label(root, text="Water Level: ", width=20, font=('Helvetica', 20), fg='black', bg='#26c6da')
water_level_label.grid(row=4, column=4, pady=20)
water_level_canvas = tk.Canvas(root, width=30, height=100, bg='white')
water_level_canvas.grid(row=6, column=4)
water_level_bar = water_level_canvas.create_rectangle(0, 100, 30, 100, fill="white")
water_level_bar2 = water_level_canvas.create_rectangle(0, 100, 30, 0, fill="blue")


# Create refill status label and icon
refill_label = tk.Label(root, text="Water Refill: OFF", width=20, font=('Helvetica', 20, 'bold'), bd=2, bg='#26c6da', fg='black')
refill_label.grid(row=7, column=4)
refill_icon = tk.Canvas(root, width=30, height=30, bg='#e0f7fa', bd=2, relief='solid')
refill_icon.grid(row=8, column=4)
refill_icon.create_oval(5, 5, 34, 34, fill="red", tags="icon")


# Create frames for control systems with labels and icons
def create_system_frame(system_name, row, col, bg_color):
    # Create a frame for the system control with a border color
    outer_frame = tk.Frame(root, bd=2, bg='#26c6da')  # This is the outer frame with the border color

    # Create a colored inner frame for the system control background
    inner_frame = tk.Frame(outer_frame, bd=2, bg=bg_color)
    inner_frame.pack(padx=5, pady=5, fill='both', expand=True)  # Adding padding inside the border

    # Create labels for system status
    status_label = tk.Label(inner_frame, text=f"{system_name}: OFF", font=('Helvetica', 20, 'bold'), width=20, bg=bg_color, fg='black', bd=4, relief='solid')
    status_label.grid(row=0, column=0, pady=20)

    # Create icon canvas
    icon_canvas = tk.Canvas(inner_frame, width=30, height=30, bg='#e0f7fa', bd=2, relief='solid')
    icon_canvas.grid(row=0, column=1)
    icon_canvas.create_oval(5, 5, 34, 34, fill="red", tags="icon")

    # Place the outer frame in the grid
    outer_frame.grid(row=row, column=col)

    return status_label, icon_canvas


# Define colors
fan_color = '#ff7043'    # Coral Orange
heater_color = '#00796b' # Deep Teal
irrigation_color = '#ffca28' # Bright Yellow
lights_color = '#8e24aa' # Purple

fan_label, fan_icon = create_system_frame("Fan", 0, 0, fan_color)
heater_label, heater_icon = create_system_frame("Heater", 1, 0, heater_color)
irrigation_label, irrigation_icon = create_system_frame("Irrigation", 2, 0, irrigation_color)
lights_label, light_icon = create_system_frame("Light", 3, 0, lights_color)


# Create crop selection dropdown menu
crop_selection = tk.StringVar()
crop_selection.set("Select Crop")

# Create an OptionMenu with a colored border
crop_menu = tk.OptionMenu(root, crop_selection, *crop_data.keys())
crop_menu.config(bd=0, font=('Helvetica', 18), width=20, height=0, highlightbackground="#26c6da", highlightcolor="#26c6da", highlightthickness=0)
crop_menu.grid(row=0, column=9)

# Button to confirm crop selection and display planting start date with a colored border
select_crop_button = tk.Button(root, text="Select Crop", font=('Arial', 18), width=20, command=select_crop, fg='black', bg='#26c6da', bd=5, highlightbackground="#26c6da", highlightcolor="#26c6da", highlightthickness=5)
select_crop_button.grid(row=1, column=9)


# Current month label
#current_month_label = tk.Label(root, text="Current Month: ", width=25, font=('Helvetica', 18), fg='black', bg='#26c6da')
#current_month_label.grid(row=2, column=9)


# Label to show planting start date
#planting_label = tk.Label(root, text="Planting Start Date: ", width=25, font=('Helvetica', 18), fg='black', bg='#26c6da')
#planting_label.grid(row=3, column=9)


# Label to show harvesting month
#harvesting_label = tk.Label(root, text="Harvesting Month: ", width=25, font=('Helvetica', 18), fg='black', bg='#26c6da')
#harvesting_label.grid(row=4, column=9)


# Simulation time and part of day labels
simulation_time_label = tk.Label(root, text="Simulation Time: ", width=25, font=('Helvetica', 18), fg='black', bg='#26c6da')
simulation_time_label.grid(row=2, column=9)
day_period_label = tk.Label(root, text="Part of Day: ", width=25, font=('Helvetica', 18), fg='black', bg='#26c6da')
day_period_label.grid(row=3, column=9)


# Start simulation button
start_button = tk.Button(root, text="Start Simulation", width=40, font=('Arial', 26), command=start_simulation, fg='black', bg='#26c6da')
start_button.grid(row=9, columnspan=15)

tomato_image_label = tk.Label(root, bg='#26c6da')
tomato_image_label.grid(row=12, column=4, rowspan=6)


# Start the Tkinter main loop
root.mainloop()

