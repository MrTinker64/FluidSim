import numpy as np
import time

width, height = 10, 10 

physical_width = 1  # e.g., 1 meter
physical_height = 1  # e.g., 1 meter this means were simulating fluid in a 1m x 1m space

h_x = physical_width / (width - 1)  # the space between points on the x-axis
h_y = physical_height / (height - 1)  # the space between points on the y-axis
#TODO add boundary cells
h = h_x + h_y / 2

grid = np.zeros((height, width, 2))

u_velocity = np.zeros((height, width + 1))  # horizontal velocity, located on the vertical faces of the cells
v_velocity = np.zeros((height + 1, width))  # vertical velocity, located on the horizontal faces of the cells
s = np.zeros(height, width) # s (used in divergence calculations)

for i in range(height):
    for j in range(width):
        grid[i, j] = [0, 0] # initalizes pressure and density as 0
        
u_velocity[:, :] = 0 # initalizes u_velocities as 0
v_velocity[:, :] = 0 # initalizes v_velocities as 0
        
total_simulation_time = 10.0  # 10 seconds
dt = 0.01  # 0.01 seconds (10 milliseconds)
current_simulation_time = 0.0

g = 9.81 # gravity
o = 1.9 # Overrelaxation

def compute_next_state():
    modify_velocity_values()
    projection()
    advectVel()

def modify_velocity_values():
    v_velocity[1:-1, :] += g * dt  

def projection():
    for i in range(height):
        for j in range(width):
            if s[i,j] == 0:
                continue
            
            s = s[i,j]
            sx0 = s[i-1,j]
            sx1 = s[i+1,j]
            sy0 = s[i,j-1]
            sy1 = s[i,j+1]
            s = sx0 + sx1 + sy0 + sy1
            if (s == 0.0):
                continue
            
            div = o(u_velocity[i+1,j] - u_velocity[i,j] + v_velocity[i,j+1] - v_velocity[i,j])

            u_velocity[i,j] += div * sx0 / s
            u_velocity[i+1,j] -= div * sx1
            v_velocity[i,j] += div * sy0
            v_velocity[i,j+1] -= div * sy1
            
            grid[i,j,1] += div / s * (grid[i,j,2] * h) / dt

def avgU(i, j):
    u = (u_velocity[i,j-1] + u_velocity[i,j] + u_velocity[i,j-1] + u_velocity[i+1,j]) / 4
    return u

def avgV(i, j):
    v = (v_velocity[i,j-1] + v_velocity[i,j] + v_velocity[i,j-1] + v_velocity[i+1,j]) / 4
    return v

def advectVel():
    newU = u_velocity
    newV = v_velocity
    
    for i in range(height):
        for j in range(width):
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