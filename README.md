# Autonomous Car Lane & Speed Optimization

## Overview
This project is a simulation of an autonomous car navigating a road while optimizing its lane and speed using Constraint Programming (CP) with Google's OR-Tools. The simulation is visualized using Tkinter, showcasing real-time lane and speed adjustments to avoid obstacles and ensure smooth driving.

## Features
- **Graphical simulation with Tkinter**: Displays the autonomous car moving through lanes.
- **Constraint Programming Optimization**: Uses OR-Tools to determine the optimal speed and lane changes.
- **Obstacle Avoidance**: Ensures the car avoids obstacles at specific time steps.
- **Real-time visualization**: Displays the car's speed, lane changes, and time progression.

## Installation
### Prerequisites
Ensure you have Python installed (version 3.7+ recommended). You also need the following libraries:

```sh
pip install ortools tkinter
```

## How to Run
1. Run the Python script:

   ```sh
   python autonomous_car_simulation.py
   ```

2. Click the **Start Simulation** button to begin the car's movement.
3. The car will change lanes and adjust speed based on optimization results.
4. The simulation runs for 10 time steps and stops automatically.

## Components
- **Tkinter GUI**: Provides a visual representation of the road, car, and obstacles.
- **Constraint Programming Model**: Determines the best lane and speed adjustments.
- **Obstacle Handling**: Ensures the car does not occupy a blocked lane.

## Road Map
- Extend the model to incorporate dynamic obstacles.
- Implement real-world traffic rules.
- Integrate reinforcement learning for adaptive driving decisions.

## Author
Created by Mohamed Esam.

