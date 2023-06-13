import pygame
import math
import matplotlib.pyplot as plt
import random

WIDTH, HEIGHT = 800, 800
RADIUS = 300
CENTRE = (WIDTH//2, HEIGHT//2)
NUM_AGENTS = 20
MAX_ACCELERATION = 0.001
SLOW_SPEED = 0.005
CLOSE_DISTANCE = 50
WHITE = (255, 255, 255)
RED = (255, 0, 0)
MAX_SPEED = 5

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))

class Agent:
    def __init__(self, angle):
        self.angle = angle
        self.x = CENTRE[0] + RADIUS * math.cos(self.angle)
        self.y = CENTRE[1] + RADIUS * math.sin(self.angle)
        self.speeds = []
        self.speed = 0
        self.acceleration = random.uniform(0, MAX_ACCELERATION) 

    def update(self, next_agent):
        distance_to_next = math.sqrt((self.x - next_agent.x)**2 + (self.y - next_agent.y)**2)
        if distance_to_next < CLOSE_DISTANCE:
            speed = SLOW_SPEED
        else:
            self.speed += self.acceleration  
            speed = min(self.speed, MAX_SPEED)  
        self.speeds.append(speed) 
        self.angle += math.radians(speed)
        self.x = CENTRE[0] + RADIUS * math.cos(self.angle)
        self.y = CENTRE[1] + RADIUS * math.sin(self.angle)

    def draw(self, win):
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), 10)


agents = [Agent(i * 2 * math.pi / NUM_AGENTS) for i in range(NUM_AGENTS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((0, 0, 0))

    
    pygame.draw.circle(win, WHITE, CENTRE, RADIUS, 2)

    for i in range(NUM_AGENTS):
        agents[i].update(agents[(i+1) % NUM_AGENTS])
        agents[i].draw(win)

    pygame.display.flip()

pygame.quit()

plt.figure()
for i, agent in enumerate(agents):
    plt.plot(agent.speeds, label=f"Agent {i+1}")
plt.legend()
plt.xlabel("Time")
plt.ylabel("Speed")
plt.title("Speed of each agent over time")
plt.show()
