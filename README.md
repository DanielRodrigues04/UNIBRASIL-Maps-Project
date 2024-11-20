# UNIBRASIL Maps Project

## Overview

UNIBRASIL Maps is a Python-based project designed to optimize drone flight routes for mapping locations efficiently. The application calculates optimal paths, manages resources like battery life, and adapts to environmental conditions to achieve the goal of mapping postal codes in Curitiba.

## Features

- **Distance Calculation**: Uses the Haversine formula to compute distances between coordinates.
- **Wind Adaptation**: Adjusts the drone's speed based on wind conditions.
- **Battery Management**: Monitors and optimizes battery usage during flights.
- **Postal Code Mapping**: Converts postal codes into geographic coordinates for navigation.
- **Route Optimization**: Implements a genetic algorithm to find the most efficient flight path.
- **Data Output**: Generates a CSV file detailing the drone's flight path and resource usage.


## Students 
- Daniel Rodrigues
- João Pedro Amaral
- Yan Percegona Weiss


## Requirements

- Dependencies listed in `requirements.txt`

## Installation

Follow these steps to set up the project:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/USERNAME/REPOSITORY.git
   ```
   
   ```bash
   cd REPOSITORY
   ```

 ## Run and Start
   ```bash
    python main.py
   ```



## Software Architecture
```bash 
UNIBRASIL_Maps/
├── .git/                # Git metadata
├── .venv/               # Virtual environment (optional)
├── data/                # Input data files (postal codes, coordinates, etc.)
├── output/              # Generated CSV files with flight paths
├── src/                 # Source code for the project
│   ├── __init__.py      # Package initializer
│   ├── module1.py       # Example module
│   └── module2.py       # Example module
├── tests/               # Unit tests
│   ├── test_module1.py  # Unit tests for module1
│   └── test_module2.py  # Unit tests for module2
├── config.py            # Configuration file for the project
├── main.py              # Entry point of the project
├── requirements.txt     # Dependencies for the project
└── README.md            # Project documentation
```


