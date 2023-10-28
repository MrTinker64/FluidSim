import numpy as np
import time

width, height = 10, 10 

grid = np.zeros((height, width, 2))

for i in range(height):
    for j in range(width):
        grid[i, j] = [0, 0]
        
total_simulation_time = 10.0  # 10 seconds
dt = 0.01  # 0.01 seconds (10 milliseconds)
current_simulation_time = 0.0

def compute_next_state():
    modify_velocity_values()
    projection()
    advection()
    
while current_simulation_time < total_simulation_time:        
    start_real_time = time.time() # Capture the real-world time before processing    
    
    state = compute_next_state(state, dt)
    
    current_simulation_time += dt
    
    # If you want sim to run in real time
    end_real_time = time.time()
    processing_time = end_real_time - start_real_time
    if processing_time < dt:
        time.sleep(dt - processing_time)

def modify_velocity_values():
    pass

def update_velocity():
    pass

def projection():
    pass

def advection():
    pass