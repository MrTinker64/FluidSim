import numpy as np
import pygame
import sys

# Set up the constants for the simulation
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PARTICLE_COUNT = 100
PARTICLE_SIZE = 4
PARTICLE_MASS = 1
FLUID_DENSITY = 1
GRAVITY = 0.05
COLLISION_DAMPING = 0.75
SMOOTHING_RADIUS = 5

class Particle:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.zeros(2, dtype=float)
        self.acceleration = np.zeros(2, dtype=float)
        self.density = FLUID_DENSITY
        self.pressure = 0

particles = [Particle(np.random.randint(0, WINDOW_WIDTH), np.random.randint(0, WINDOW_HEIGHT)) for _ in range(PARTICLE_COUNT)]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()

    running = True
    
    last_update_time = pygame.time.get_ticks()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))  # Fill the screen with black

        current_time = pygame.time.get_ticks()
        dt = (current_time - last_update_time) / 1000.0
        
        # Update particle physics
        for particle in particles:
            compute_forces(particle, dt)

        # Render particles
        for particle in particles:
            pygame.draw.circle(screen, (255, 255, 255), (int(particle.position[0]), int(particle.position[1])), PARTICLE_SIZE)

        pygame.display.flip()
        clock.tick(60)  # Limiting to 60 frames per second (fps)
        
        print(particles[0].density)
        
        # Ends simulation after 10 seconds
        if current_time > 10000:
            return

    pygame.quit()
    sys.exit()
    
def compute_forces(particle: Particle, dt: float):
    particle.velocity += np.array([0, 1], dtype=float) * GRAVITY * dt
    particle.position += particle.velocity * dt
    resolve_collisions(particle)
    particle.density = calculate_density(particle.position)
    
def resolve_collisions(particle: Particle):
    p = particle
    bound_height = WINDOW_HEIGHT - PARTICLE_SIZE

    if (p.position[1] > bound_height):
        p.position[1] = bound_height * np.sign(p.position[1])
        p.velocity[1] *= -1 * COLLISION_DAMPING
        
def smoothing_kernel(radius: float, dst: float):
    volume = np.pi * np.power(radius, 7) / 4
    value = np.maximum(0, radius * radius - dst * dst)
    return value * value * value / volume

def calculate_density(sample_point):
    density = 0
    mass = 1
    
    # TODO optimize to only look at particles in smoothing radius
    for particle in particles:
        position = particle.position
        dst = np.linalg.norm(position - sample_point) # finds magnitude
        influence = smoothing_kernel(SMOOTHING_RADIUS, dst)
        density += mass * influence
        
    return density
        
if __name__ == "__main__":
    main()