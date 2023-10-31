import math
import numpy as np
import time

width, height = 10, 10 

physical_width = 1  # e.g., 1 meter
physical_height = 1  # e.g., 1 meter this means were simulating fluid in a 1m x 1m space

h_x = physical_width / (width - 1)  # the space between points on the x-axis
h_y = physical_height / (height - 1)  # the space between points on the y-axis
#TODO add boundary cells
h = h_x + h_y / 2

U_FIELD = 0
V_FIELD = 1
S_FIELD = 2

u_velocity = np.zeros((height, width + 1))  # horizontal velocity, located on the vertical faces of the cells
v_velocity = np.zeros((height + 1, width))  # vertical velocity, located on the horizontal faces of the cells
s = np.zeros((height, width)) # s (used in divergence calculations)
m = np.ones((height, width)) # density
rho = np.zeros((height, width)) # pressure
        
total_simulation_time = 10.0  # 10 seconds
dt = 0.01  # 0.01 seconds (10 milliseconds)
current_simulation_time = 0.0

g = 9.81 # gravity
o = 1.9 # Overrelaxation

def compute_next_state():
    modify_velocity_values()
    projection()
    advect_vel()
    advect_smoke()

def modify_velocity_values():
    v_velocity[1:-1, :] += g * dt  

def projection():
    for i in range(height):
        for j in range(width):
            if s[i,j] == 0:
                continue
            
            s_member = s[i,j]
            sx0 = s[i-1,j]
            sx1 = s[i+1,j]
            sy0 = s[i,j-1]
            sy1 = s[i,j+1]
            s_member = sx0 + sx1 + sy0 + sy1
            if (s_member == 0.0):
                continue
            
            div = o*(u_velocity[i+1,j] - u_velocity[i,j] + v_velocity[i,j+1] - v_velocity[i,j])

            u_velocity[i,j] += div * sx0 / s_member
            u_velocity[i+1,j] -= div * sx1
            v_velocity[i,j] += div * sy0
            v_velocity[i,j+1] -= div * sy1
            
            rho[i,j] += div / s_member * (m[i,j] * h) / dt
            
def sample_field(x, y, field):
    n = height
    h1 = 1.0 / h
    h2 = 0.5 * h

    x = max(min(x, width * h), h)
    y = max(min(y, height * h), h)

    dx = 0.0
    dy = 0.0

    if field == U_FIELD:
        f = u_velocity
        dy = h2
    elif field == V_FIELD:
        f = v_velocity
        dx = h2
    elif field == S_FIELD:
        f = m
        dx = h2
        dy = h2

    x0 = min(int((x - dx) * h1), width - 1)
    tx = ((x - dx) - x0 * h) * h1
    x1 = min(x0 + 1, width - 1)

    y0 = min(int((y - dy) * h1), height - 1)
    ty = ((y - dy) - y0 * h) * h1
    y1 = min(y0 + 1, height - 1)

    sx = 1.0 - tx
    sy = 1.0 - ty

    val = sx * sy * f[x0 * n + y0] + \
        tx * sy * f[x1 * n + y0] + \
        tx * ty * f[x1 * n + y1] + \
        sx * ty * f[x0 * n + y1]

    return val

def advect_vel():
    new_u = u_velocity.copy()
    new_v = v_velocity.copy()
    
    for i in range(height):
        for j in range(width + 1):
    # Compute the full velocity value at the point
        # figure out the vertical component v bar by averaging surrounding v values
            x = i * h
            y = j * h + h/2
            u = u_velocity[i,j]
            v = (v_velocity[i,j], v_velocity[i,j+1], v_velocity[i-1,j], v_velocity[i-1,j+1]) / 4
            x = x - dt*u
            y = y - dt*v
            
            u = sample_field(x, y, U_FIELD)
            
            new_u[i,j] = u
            
    for i in range(height + 1):
        for j in range(width):
            x = i * h + h/2
            y = j * h
            u = (u_velocity[i,j], u_velocity[i,j+1], u_velocity[i-1,j], u_velocity[i-1,j+1]) / 4
            v = v_velocity[i,j]
            x = x - dt*u
            y = y - dt*v
            
            v = sample_field(x, y, V_FIELD)
            
            new_v[i,j] = v
            
    u_velocity = new_u.copy()
    v_velocity = new_v.copy()
    
def advect_smoke():
    new_m = m.copy()

    n = height

    h2 = 0.5 * h

    # Iterate over all cells, excluding boundary cells.
    for i in range(height):
        for j in range(width):

            # If the cell isn't empty (i.e., has smoke or substance).
            if s[i * n + j] != 0.0:

                # Calculate average horizontal velocity in the current cell.
                u = 0.5 * (u_velocity[i * n + j] + u_velocity[(i + 1) * n + j])

                # Calculate average vertical velocity in the current cell.
                v = 0.5 * (v_velocity[i * n + j] + v_velocity[i * n + j + 1])

                # Compute the new positions based on the velocity.
                # This "traces" where the smoke would come from in the previous timestep.
                x = i * h + h2 - dt * u
                y = j * h + h2 - dt * v

                # Set the new smoke concentration/density based on the value from the traced position.
                new_m[i * n + j] = sample_field(x, y, S_FIELD)

    # Update the main smoke concentration/density array with the new values.
    m = new_m.copy()

while current_simulation_time < total_simulation_time:        
    start_real_time = time.time() # Capture the real-world time before processing    
    
    state = compute_next_state(state, dt)
    
    current_simulation_time += dt
    
    # If you want sim to run in real time
    end_real_time = time.time()
    processing_time = end_real_time - start_real_time
    if processing_time < dt:
        time.sleep(dt - processing_time)