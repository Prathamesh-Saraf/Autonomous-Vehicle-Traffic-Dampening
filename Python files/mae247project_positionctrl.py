import pygame
import random
import math
import matplotlib.pyplot as plt

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Circular Track Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define agent class
class Agent:
    def __init__(self, radius, color, speed):
        self.radius = radius
        self.color = color
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)

        # Calculate initial position on the circular track
        center_x = screen_width // 2
        center_y = screen_height // 2
        radius_track = min(center_x, center_y) - self.radius - 10
        self.position = [
            center_x + radius_track * math.cos(self.angle),
            center_y + radius_track * math.sin(self.angle)
        ]

        # Velocity history
        self.velocity_history = []

    def update(self, agents):
        desired_speed = self.speed
        desired_position = self.angle

        for i, agent in enumerate(agents):
            if agent != self:
                dx = agent.position[0] - self.position[0]
                dy = agent.position[1] - self.position[1]
                distance = math.sqrt(dx ** 2 + dy ** 2)
                min_distance = self.radius + agent.radius

                # PD control for position consensus
                k_p_position = 1  # Proportional gain for position consensus
                k_d_position = 1  # Derivative gain for position consensus
                relative_position = agent.angle - self.angle

                desired_position += k_p_position * relative_position + k_d_position * (agent.speed - self.speed)

                # PD control for velocity consensus
                k_p_velocity = 0.01  # Proportional gain for velocity consensus
                k_d_velocity = 0.001  # Derivative gain for velocity consensus
                relative_velocity = (agent.speed - self.speed) / distance

                desired_speed += k_p_velocity * (agent.speed - self.speed) + k_d_velocity * relative_velocity

        # Update speed and position
        self.speed = min(max(desired_speed, -0.06), 0.06)  # Saturation limits
        self.angle += self.speed

        # Update position on the circular track
        center_x = screen_width // 2
        center_y = screen_height // 2
        radius_track = min(center_x, center_y) - self.radius - 10
        self.position = [
            center_x + radius_track * math.cos(self.angle),
            center_y + radius_track * math.sin(self.angle)
        ]

        # Store velocity history
        self.velocity_history.append(self.speed)

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), self.radius)

# Create agents
num_agents = 10
agents = []
for _ in range(num_agents):
    radius = 20
    color = random.choice([RED, GREEN, BLUE])
    speed = random.uniform(0.01, 0.06)
    agent = Agent(radius, color, speed)
    agents.append(agent)

# Game loop
running = True
clock = pygame.time.Clock()
time_step = 0
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update agents
    for agent in agents:
        agent.update(agents)

    # Draw agents and track
    screen.fill(WHITE)
    pygame.draw.circle(screen, BLACK, (screen_width // 2, screen_height // 2), screen_height // 2 - 50, 5)
    for agent in agents:
        agent.draw()

    # Update the display
    pygame.display.update()
    clock.tick(60)

    time_step += 1

    if time_step >= 600:  # Stop the simulation after 600 time steps
        break

# Position Consensus
for _ in range(500):
    for i, agent in enumerate(agents):
        neighbor1 = agents[(i - 1) % num_agents]
        neighbor2 = agents[(i + 1) % num_agents]
        desired_position = neighbor1.angle + (2 * math.pi * agent.radius / (num_agents * neighbor1.radius))
        position_error = desired_position - agent.angle
        agent.angle += 0.1 * position_error

# Store velocity values
velocity_values = [[] for _ in range(num_agents)]
for i, agent in enumerate(agents):
    velocity_values[i] = agent.velocity_history

# Plot velocity graph
plt.figure(figsize=(8, 5))
for i, velocities in enumerate(velocity_values):
    plt.plot(range(len(velocities)), velocities, label=f"Agent {i+1}")

plt.xlabel("Time Step")
plt.ylabel("Velocity")
plt.title("Agent Velocity over Time")
plt.legend()
plt.grid(True)
plt.show()

# Quit the program
pygame.quit()




