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
GRAVITY = 1

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

    pygame.quit()
    sys.exit()
    
def compute_forces(particle: Particle, dt: float):
    particle.velocity += np.array([0, 1], dtype=float) * GRAVITY * dt
    particle.position += particle.velocity * dt
        
if __name__ == "__main__":
    main()