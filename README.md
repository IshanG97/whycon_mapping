# WhyCon Localisation and Mapping Algorithm
**Winner of the 2020 University of Manchester 4th Year Project Prize**

A Python-based mapping and localisation system using WhyCon visual markers for autonomous robot navigation. The system creates real-time occupancy grid maps and provides precise robot positioning through computer vision and sensor fusion techniques.

## Features

- **WhyCon Visual Localisation**: Tracks circular markers for precise robot positioning
- **Grid-Based Mapping**: Creates occupancy grid maps with different cell types (obstacles, mines, paths)
- **Multi-Platform Support**: Includes Android app for mobile deployment
- **Real-Time Visualization**: Generates both PNG and SVG map outputs
- **Sensor Integration**: Processes data from ultrasound sensors and MD/GPR sensors

## Project Structure

```
whycon_mapping/
├── pose.py                    # Core pose processing and grid map data management
├── mapping.py                 # Map generation and visualization functions
├── android_app/               # Android application for mobile deployment
│   └── src/                   # Android source code
├── marker_locations.txt       # Marker position data
├── pose_history_1.txt         # Robot pose tracking data
├── mine_locations_1.txt       # Mine detection coordinates
└── whycon_log_1.txt          # System operation logs
```

## Cell Types

The mapping system uses a grid-based representation with different cell types:

- **Empty Cell (0)**: Unoccupied space
- **Start Cell (1)**: Starting position  
- **Goal Cell (2)**: Target destination
- **Path Cell (3)**: Traversed path
- **Obstacle Cell (4)**: Detected obstacles
- **Mine Cell (5)**: Mine detection points
- **Roundel Cell (6)**: Marker locations
- **Buggy Cell (8)**: Current robot position

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd whycon_mapping
   ```

2. Install dependencies:
   ```bash
   pip install numpy matplotlib pathlib
   ```

3. Run the mapping system:
   ```bash
   python mapping.py
   ```

## Technology Stack

- **Backend**: Python, NumPy, Matplotlib
- **Computer Vision**: WhyCon marker detection
- **Mobile**: Android (C++)
- **Visualization**: PNG and SVG map generation

## Usage

The system processes sensor data and generates maps in real-time, supporting autonomous navigation in structured environments. Map output can be customized for different grid sizes and visualization requirements.

## License

This project was developed as part of university coursework and won the 2020 University Project Prize.

## Author

Ishan Godawatta, University of Manchester, 2020
