import numpy as np
import time

width, height = 10, 10 

grid = np.zeros((height, width, 1))

u_velocity = np.zeros((height, width + 1))  # horizontal velocity, located on the vertical faces of the cells
v_velocity = np.zeros((height + 1, width))  # vertical velocity, located on the horizontal faces of the cells

for i in range(height):
    for j in range(width):
        grid[i, j] = [0] # initalizes divergence as 0
        
u_velocity[:, :] = 0 # initalizes u_velocities as 0
v_velocity[:, :] = 0 # initalizes v_velocities as 0
        
total_simulation_time = 10.0  # 10 seconds
dt = 0.01  # 0.01 seconds (10 milliseconds)
current_simulation_time = 0.0

g = 9.81

def compute_next_state():
    modify_velocity_values()
    projection()
    advection()

def modify_velocity_values():
    v_velocity[1:-1, :] += g * dt  

def projection():
    for i in range(height):
        for j in range(width):
            divergence = u_velocity[i+1,j] - u_velocity[i,j] + v_velocity[i,j+1] - v_velocity[i,j]
            grid[i, j, 1] = [divergence]

def advection():
    pass

while current_simulation_time < total_simulation_time:        
    start_real_time = time.time() # Capture the real-world time before processing    
    
    state = compute_next_state(state, dt)
    
    current_simulation_time += dt
    
    # If you want sim to run in real time
    end_real_time = time.time()
    processing_time = end_real_time - start_real_time
    if processing_time < dt:
        time.sleep(dt - processing_time)