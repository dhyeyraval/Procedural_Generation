import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from matplotlib.colors import ListedColormap

# Step 1: Base Terrain

def generate_base_terrain(width=32, height=32, scale=10.0, seed=42):

    terrain_map = np.zeros((height, width))

    noise_gen = PerlinNoise(octaves=1, seed=seed)

    for y in range(height):
        for x in range(width):
            noise_val = noise_gen([x/scale, y/scale])

            if noise_val < 0.0:
                terrain_map[y][x] = 0 # deep water
            else:
                terrain_map[y][x] = 1 # shallow rock

    return terrain_map

def plot_and_save_map(terrain_map, filename="step1_terrain.png"):

    plt.figure(figsize=(5, 5))

    plt.imshow(terrain_map, cmap='Blues_r', interpolation='nearest', vmin=0, vmax=1.5)

    plt.title("Step 1: Base Terrain (Depth)")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 2: Water Current Map

def generate_current_map(width=32, height=32, scale=20.0, seed=1337):

    current_map = np.zeros((height, width))

    noise_gen = PerlinNoise(octaves=1, seed=seed)

    for y in range(height):
        for x in range(width):
            noise_val = noise_gen([x/scale, y/scale])

            if noise_val < 0.0:
                current_map[y][x] = 0 # calm water
            else:
                current_map[y][x] = 1 # strong water

    return current_map

def plot_current_map(current_map, filename="step2_current.png"):

    plt.figure(figsize=(5, 5))

    plt.imshow(current_map, cmap='Purples', interpolation='nearest', vmin=0, vmax=1.5)

    plt.title("Step 2: Water Current (Flow)")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 3: Biome Matrix

def generate_biome_map(terrain_map, current_map):
    # 0 = deep calm
    # 1 = deep flow
    # 2 = sheltered rock
    # 3 = exposed reef
    biome_map = (terrain_map * 2) + current_map
    return biome_map

def plot_biome_map(biome_map, filename='step3_biomes.png'):

    plt.figure(figsize=(6, 6))

    custom_colours = [
        '#08306b', # deep calm - dark blue
        '#2879b9', # deep flow - teal
        '#d2b48c', # sheltered rock - beige
        '#ff7f50', # exposed reef - orange
    ]
    cmap = ListedColormap(custom_colours)
    
    plt.imshow(biome_map, cmap=cmap, interpolation='nearest', vmin=0, vmax=3)

    plt.title("Step 3: Biome Matrix (Combined Data)")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 4: Coral Placement and Clustering

def generate_coral_placement(biome_map, seed=42, spawn_attempts=20, cluster_size=2):
    
    height, width = biome_map.shape
    coral_map = np.zeros((height, width), dtype=int)

    rng = np.random.default_rng(seed)

    for _ in range(spawn_attempts):
        x = rng.integers(0, width)
        y = rng.integers(0, height)

        if coral_map[y, x] == 0:
            if biome_map[y, x] == 3:
                coral_map[y, x] = 1 # spawn staghorn parent
            elif biome_map[y, x] == 2:
                coral_map[y, x] = 2 # spawn brain coral parent

    for _ in range(cluster_size):
        current_corals = coral_map.copy()

        for y in range(height):
            for x in range(width):
                if current_corals[y, x] != 0:
                    coral_type = current_corals[y, x]
                    required_biome = 3 if coral_type == 1 else 2

                    neighbours = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]

                    for ny, nx in neighbours:
                        if 0 <= ny < height and 0 <= nx < width:
                            if coral_map[ny, nx] == 0 and biome_map[ny, nx] == required_biome:
                                coral_map[ny, nx] = coral_type

    return coral_map

def plot_ecosystem(biome_map, coral_map, filename="step4_ecosystem.png"):

    height, width = biome_map.shape
    viz_map = np.zeros((height, width), dtype=int)

    for y in range(height):
        for x in range(width):
            if coral_map[y, x] == 1:
                viz_map[y, x] = 4 # staghorn coral indicator
            elif coral_map[y, x] == 2:
                viz_map[y, x] = 5 # brain coral indicator
            else:
                viz_map[y, x] = biome_map[y, x]

    plt.figure(figsize=(6, 6))

    custom_colours = [
        '#08306b', # deep calm
        '#2879b9', # deep flow
        '#d2b48c', # sheltered rock
        '#ff7f50', # exposed reef
        '#ff00ff', # staghorn
        '#00ff00', # brain
    ]
    cmap = ListedColormap(custom_colours)

    plt.imshow(viz_map, cmap=cmap, interpolation='nearest', vmin=0, vmax=5)

    plt.title("Step 4: Coral Placement and Clustering")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":

    my_terrain = generate_base_terrain(seed=42)
    plot_and_save_map(my_terrain)

    my_current = generate_current_map(seed=1337)
    plot_current_map(my_current)

    my_biomes = generate_biome_map(my_terrain, my_current)
    plot_biome_map(my_biomes)

    my_corals = generate_coral_placement(my_biomes, seed=42)
    plot_ecosystem(my_biomes, my_corals)