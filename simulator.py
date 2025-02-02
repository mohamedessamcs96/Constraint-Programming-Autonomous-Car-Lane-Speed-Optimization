import tkinter as tk
from ortools.sat.python import cp_model

class RoadSimulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autonomous Car Simulation")

        # Canvas for the road
        self.canvas = tk.Canvas(root, width=600, height=400, bg='lightgray')
        self.canvas.pack()

        # Variables to simulate road and car
        self.car = None
        self.car_wheels = []  # List to store wheels
        self.car_windows = []  # List to store windows
        self.lanes = [100, 250, 400]  # Lane positions on the canvas
        self.time_step = 0
        self.time_steps = 10
        self.speeds = []
        self.lanes_used = []
        self.car_x = 50  # Initial car x-position (time step 0)

        # Labels to display time and speed
        self.time_label = tk.Label(root, text="Time: 0", font=("Arial", 14))
        self.time_label.pack()
        self.speed_label = tk.Label(root, text="Speed: 0 km/h", font=("Arial", 14))
        self.speed_label.pack()
        self.lane_label = tk.Label(root, text="Lane at t=5: N/A", font=("Arial", 14))
        self.lane_label.pack()


        # Title and description
        self.canvas.create_text(300, 50, text="Autonomous Car Lane & Speed Optimization", font=("Arial", 18, "bold"), fill="blue")
        self.canvas.create_text(300, 100, text="Optimize an autonomous car's lane & speed decisions.", font=("Arial", 14), fill="black")
        self.canvas.create_text(300, 150, text="Navigate through lanes, avoid obstacles, and optimize speed.", font=("Arial", 12), fill="black")
        self.canvas.create_text(300, 200, text="Welcome to the world of intelligent transportation systems!", font=("Arial", 12), fill="black")
        self.canvas.create_text(300, 250, text="Created by Mohamed Esam", font=("Arial", 10), fill="gray")

        # Buttons
        self.start_button = tk.Button(root, text="Start Simulation", command=self.start_simulation, font=("Arial", 12))
        self.start_button.pack(pady=10)

    


    def draw_road(self):
        # Draw lanes on the road
        self.canvas.create_line(50, 100, 550, 100, width=2, fill='white', dash=(5, 2))  # Top lane line (dashed)
        self.canvas.create_line(50, 250, 550, 250, width=2, fill='white', dash=(5, 2))  # Middle lane line (dashed)
        self.canvas.create_line(50, 400, 550, 400, width=2, fill='white', dash=(5, 2))  # Bottom lane line (dashed)

        # Draw obstacles on the road (e.g., at time t=5 and lane 2)
        self.canvas.create_rectangle(300, 230, 350, 270, fill="red", outline="black", width=2)
        # Adding a "tree" or "barrier" for better road features
        self.canvas.create_oval(500, 230, 530, 260, fill="green", outline="black")

    def draw_car(self, lane, speed):
        # Update car's x-position based on speed and time_step for smoother movement
        car_x = 50 + (self.time_step * speed)
        car_y = self.lanes[lane - 1]  # Using lane as an index

        # Delete the previous car, wheels, and windows before drawing the new car
        if self.car:
            self.canvas.delete(self.car)  # Remove previous car
        if self.car_wheels:
            for wheel in self.car_wheels:
                self.canvas.delete(wheel)  # Remove previous wheels
        if self.car_windows:
            for window in self.car_windows:
                self.canvas.delete(window)  # Remove previous windows

        # Drawing a more realistic car with windows and wheels
        self.car = self.canvas.create_rectangle(
            car_x, car_y - 15, car_x + 40, car_y + 15, fill="blue", outline="black", width=2
        )

        # Create windows and wheels only once and store their IDs
        self.car_windows = [
            self.canvas.create_rectangle(car_x + 5, car_y - 10, car_x + 15, car_y, fill="white"),  # Left window
            self.canvas.create_rectangle(car_x + 25, car_y - 10, car_x + 35, car_y, fill="white")  # Right window
        ]
        self.car_wheels = [
            self.canvas.create_oval(car_x + 5, car_y + 10, car_x + 15, car_y + 20, fill="black"),  # Left wheel
            self.canvas.create_oval(car_x + 25, car_y + 10, car_x + 35, car_y + 20, fill="black")  # Right wheel
        ]

    def update_simulation(self):
        # Update the car's position and display at each time step
        if self.time_step < self.time_steps:
            speed = self.speeds[self.time_step]
            lane = self.lanes_used[self.time_step]
            self.draw_car(lane, speed)

            # Update the time, speed, and lane information
            self.time_label.config(text=f"Time: {self.time_step}")
            self.speed_label.config(text=f"Speed: {speed} km/h")

            if self.time_step == 5:
                self.lane_label.config(text=f"Lane at t=5: {lane}")

            self.time_step += 1
            self.root.after(500, self.update_simulation)  # Wait 500ms before next step
        else:
            print("Simulation completed.")

    def start_simulation(self):
        self.time_step = 0
        self.car_x = 50  # Reset car's initial position
        self.speeds, self.lanes_used = self.run_optimization()  # Run the optimization and get values
        self.canvas.delete("all")  # Clear the canvas for a new simulation
        self.draw_road()
        self.update_simulation()

        # Enable  button after starting the simulation
     
        self.start_button.config(state=tk.DISABLED)


    

    def run_optimization(self):
        model = cp_model.CpModel()

        # Variables
        max_speed = 120  # km/h
        min_speed = 30   # km/h
        lane_positions = [1, 2, 3]  # Available lanes
        time_steps = 10  # Planning horizon

        speed = [model.NewIntVar(min_speed, max_speed, f'speed_t{i}') for i in range(time_steps)]
        lane = [model.NewIntVar(min(lane_positions), max(lane_positions), f'lane_t{i}') for i in range(time_steps)]

        # Constraints
        for t in range(1, time_steps):
            model.Add(speed[t] - speed[t - 1] <= 30)  # Gradual speed change constraint
            model.Add(speed[t - 1] - speed[t] <= 30)  # Gradual speed change constraint

            lane_diff = model.NewIntVar(-1, 1, f'lane_diff_t{t}')
            model.Add(lane_diff == lane[t] - lane[t - 1])  # Lane change constraint

        model.Add(lane[5] != 2)  # Obstacle avoidance at time step 5

        lane_changes = [model.NewBoolVar(f'lane_change_t{t}') for t in range(1, time_steps)]
        for t in range(1, time_steps):
            model.Add(lane[t] != lane[t - 1]).OnlyEnforceIf(lane_changes[t - 1])

        model.Add(sum(lane_changes) >= 1)  # At least one lane change
        model.Add(sum(lane_changes) <= 8)  # Allow enough flexibility

        model.Maximize(sum(speed) - 2 * sum(lane_changes))  # Maximize speed with smooth lane changes

        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.log_search_progress = True
        status = solver.Solve(model)

        speeds = []
        lanes_used = []
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for t in range(time_steps):
                speeds.append(solver.Value(speed[t]))
                lanes_used.append(solver.Value(lane[t]))
        else:
            print("No feasible solution found. Adjust constraints.")

        return speeds, lanes_used


if __name__ == "__main__":
    root = tk.Tk()
    app = RoadSimulationApp(root)
    root.mainloop()
