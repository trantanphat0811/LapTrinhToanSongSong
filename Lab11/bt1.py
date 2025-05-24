from multiprocessing import Process
from collections import defaultdict
import numpy as np

# Hàm mục tiêu Rastrigin
def rastrigin(x):
    return 10 * len(x) + sum((xi * xi - 10 * np.cos(2 * np.pi * xi)) for xi in x)

class Particle:
    def __init__(self, bounds):
        self.position = np.random.uniform(bounds[0], bounds[1], len(bounds))
        self.velocity = np.random.uniform(-1, 1, len(bounds))
        self.pbest_position = self.position.copy()
        self.pbest_value = float('inf')

    def update_velocity(self, gbest_position, w=0.5, c1=1.0, c2=1.5):
        r1 = np.random.rand(len(self.position))
        r2 = np.random.rand(len(self.position))
        cognitive_velocity = c1 * r1 * (self.pbest_position - self.position)
        social_velocity = c2 * r2 * (gbest_position - self.position)
        self.velocity = w * self.velocity + cognitive_velocity + social_velocity

    def update_position(self, bounds):
        self.position += self.velocity
        self.position = np.clip(self.position, bounds[0], bounds[1])

def particle_swarm_optimization(bounds, n_particles=30, max_iter=100):
    particles = [Particle(bounds) for _ in range(n_particles)]
    gbest_value = float('inf')
    gbest_position = np.random.uniform(bounds[0], bounds[1], len(bounds))

    for _ in range(max_iter):
        for particle in particles:
            fitness = rastrigin(particle.position)
            if fitness < particle.pbest_value:
                particle.pbest_value = fitness
                particle.pbest_position = particle.position.copy()
            if fitness < gbest_value:
                gbest_value = fitness
                gbest_position = particle.position.copy()

        for particle in particles:
            particle.update_velocity(gbest_position)
            particle.update_position(bounds)

    return gbest_position, gbest_value

# Hàm bọc để chạy trong tiến trình
def run_optimization(bounds, n_particles, max_iter):
    best_position, best_fitness = particle_swarm_optimization(bounds, n_particles, max_iter)
    print("Best solution:", best_position)
    print("Best fitness:", best_fitness)

if __name__ == '__main__':
    bounds = np.array([-5.12, 5.12]) * 10
    p = Process(target=run_optimization, args=(bounds, 30, 100))
    p.start()
    p.join()