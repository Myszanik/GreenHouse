# Smart Greenhouse System

This repository contains a simple Smart Greenhouse simulation built using Python and `tkinter`. The app lets you select a crop and then simulates sensor readings (temperature, humidity, soil moisture, light). Based on the readings it automatically switches systems ON/OFF (fan, heater, irrigation, lights). It also simulates a water tank that refills automatically when it gets low.

## Overview

The Smart Greenhouse System provides a GUI where you can:
- Select a crop (Tomato, Cucumber, Strawberry)
- View simulated sensor values that change by time of day
- See the ideal ranges for each crop
- Watch automatic control logic turn systems ON/OFF
- Track tank water level and see an automatic refill when low
- Display crop growth stage images from the `assets/` folder

## Features

- **Crop Selection**
  - Tomato
  - Cucumber
  - Strawberry

- **Simulated Sensors**
  - Temperature (°C)
  - Humidity (%)
  - Soil moisture (%)
  - Light (Lux)

- **Automated Control Systems**
  - Fan
  - Heater
  - Irrigation
  - Light

- **Water Tank Simulation**
  - Tank water level display
  - Automatic refill when low

- **Growth Stage Images**
  - Loads crop images from `assets/<CropName>/stageX...png`
  - Updates stage as the simulation progresses

## Requirements

- Python 3.x
- `tkinter` (usually comes pre-installed with Python)

Python packages (installed via `requirements.txt`):
- `Pillow`

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Myszanik/GreenHouse.git
2. **Navigate to the Project Directory**
   ```bash
   cd <GreenHouse>
3. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
4. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
5. **Install Dependencies**
   ```bash
   python -m pip install -r requirements.txt
6. **Run the Application**
   ```bash
   python3 GreenHouse.py

## Notes
- Make sure the `assets/` folder exists and includes the crop image stages, otherwise the app may fail when it tries to load images.
- Simulation speed is controlled by `time_per_hour` in the code (default is 1 second = 1 simulated hour).
- The simulation currently stops when the “Ready to Harvest” button becomes available.

## Acknowledgements
- `tkinter`, for the GUI
- `Pillow`, for loading and displaying crop images

## Status
This project is for learning and practice. Improvements and clean-ups are welcome.