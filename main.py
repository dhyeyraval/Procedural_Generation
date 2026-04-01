import numpy as np
import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from matplotlib.colors import ListedColormap

# Step 1

def generate_base_terrain(width=32, height=32, scale=10.0, seed=42, octaves=1):
    terrain_map = np.zeros((height, width))

    noise_gen = PerlinNoise(octaves=octaves, seed=seed)

    for y in range(height):
        for x in range(width):
            noise_val = noise_gen([x/scale, y/scale])

            if noise_val < 0.0:
                terrain_map[y][x] = 0
            else:
                terrain_map[y][x] = 1

    return terrain_map

def plot_and_save_map(terrain_map, filename="step1_terrain.png"):

    plt.figure(figsize=(5, 5))

    plt.imshow(terrain_map, cmap='Blues_r', interpolation='nearest', vmin=0, vmax=1.5)

    plt.title("Step 1: Base Terrain (Depth)")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 2

def generate_current_map(width=32, height=32, scale=20.0, seed=1337, octaves=1):
    current_map = np.zeros((height, width))

    noise_gen = PerlinNoise(octaves=octaves, seed=seed)

    for y in range(height):
        for x in range(width):
            noise_val = noise_gen([x/scale, y/scale])

            if noise_val < 0.0:
                current_map[y][x] = 0
            else:
                current_map[y][x] = 1

    return current_map

def plot_current_map(current_map, filename="step2_current.png"):

    plt.figure(figsize=(5, 5))

    plt.imshow(current_map, cmap='Purples', interpolation='nearest', vmin=0, vmax=1.5)

    plt.title("Step 2: Water Current (Flow)")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 3

def generate_biome_map(terrain_map, current_map):
    biome_map = (terrain_map * 2) + current_map
    return biome_map

def plot_biome_map(biome_map, filename='step3_biomes.png'):

    plt.figure(figsize=(6, 6))

    custom_colours = [
        '#08306b',
        '#2879b9',
        '#d2b48c',
        '#ff7f50',
    ]
    cmap = ListedColormap(custom_colours)
    
    plt.imshow(biome_map, cmap=cmap, interpolation='nearest', vmin=0, vmax=3)

    plt.title("Step 3: Biome Matrix (Combined Data)")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 4

def generate_coral_placement(biome_map, seed=42, spawn_attempts=20, cluster_size=2):
    height, width = biome_map.shape
    coral_map = np.zeros((height, width), dtype=int)

    rng = np.random.default_rng(seed)

    for _ in range(spawn_attempts):
        x = rng.integers(0, width)
        y = rng.integers(0, height)

        if coral_map[y, x] == 0:
            if biome_map[y, x] == 3:
                coral_map[y, x] = 1
            elif biome_map[y, x] == 2:
                coral_map[y, x] = 2

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
                viz_map[y, x] = 4
            elif coral_map[y, x] == 2:
                viz_map[y, x] = 5
            else:
                viz_map[y, x] = biome_map[y, x]

    plt.figure(figsize=(6, 6))

    custom_colours = [
        '#08306b',
        '#2879b9',
        '#d2b48c',
        '#ff7f50',
        '#ff00ff',
        '#00ff00',
    ]
    cmap = ListedColormap(custom_colours)

    plt.imshow(viz_map, cmap=cmap, interpolation='nearest', vmin=0, vmax=5)

    plt.title("Step 4: Coral Placement and Clustering")
    plt.xticks([])
    plt.yticks([])

    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 5
def simulate_generation(biome_map, coral_map, rng):
    height, width = biome_map.shape
    next_coral = coral_map.copy()

    for y in range(height):
        for x in range(width):
            current_state = coral_map[y, x]
            biome = biome_map[y, x]

            neighbours = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
            valid_neighbours = [(ny, nx) for ny, nx in neighbours if 0 <= ny < height and 0 <= nx < width]

            if current_state == 0:
                adj_corals = [coral_map[ny, nx] for ny, nx in valid_neighbours if coral_map[ny, nx] != 0]

                if adj_corals:
                    if biome == 3 and 1 in adj_corals:
                        if rng.random() < 0.4:
                            next_coral[y, x] = 1
                    elif biome == 2 and 2 in adj_corals:
                        if rng.random() < 0.2:
                            next_coral[y, x] = 2

            else:
                surrounding_corals = sum(1 for ny, nx in valid_neighbours if coral_map[ny, nx] != 0)
                if surrounding_corals >= 3:
                    if rng.random() < 0.05:
                        next_coral[y, x] = 0

    return next_coral

def plot_evolution(biome_map, history, filename="step5_evolution.png"):
    fig, axes = plt.subplots(1, len(history), figsize=(15, 5))

    custom_colours = [
        '#08306b',
        '#2879b9',
        '#d2b48c',
        '#ff7f50',
        '#ff00ff',
        '#00ff00',
    ]
    cmap = ListedColormap(custom_colours)
    titles = ["Gen" + str(i) for i in range(len(history))]

    for i, ax in enumerate(axes):
        coral_map = history[i]

        height, width = biome_map.shape
        viz_map = np.zeros((height, width), dtype=int)
        for y in range(height):
            for x in range(width):
                if coral_map[y, x] == 1:
                    viz_map[y, x] = 4
                elif coral_map[y, x] == 2:
                    viz_map[y, x] = 5
                else:
                    viz_map[y, x] = biome_map[y, x]

        ax.imshow(viz_map, cmap=cmap, interpolation='nearest', vmin=0, vmax=5)
        ax.set_title(titles[i])
        ax.set_xticks([])
        ax.set_yticks([])

    plt.tight_layout()
    plt.savefig(filename, bbox_inches='tight')
    plt.show()

# Step 6

def plot_3d_map(biome_map, coral_map, filename="3d_map.png"):
    height_grid, width_grid = biome_map.shape

    z_data = np.zeros((height_grid, width_grid))
    colour_data = np.empty((height_grid, width_grid), dtype=object)
    colours = [
        '#08306b',
        '#2879b9',
        '#d2b48c',
        '#ff7f50',
        '#ff00ff',
        '#00ff00',
    ]

    for y in range(height_grid):
        for x in range(width_grid):
            if coral_map[y, x] == 1:
                z_data[y, x] = 2.0
                colour_data[y, x] = colours[4]
            elif coral_map[y, x] == 2:
                z_data[y, x] = 2.0
                colour_data[y, x] = colours[5]
            else:
                biome = biome_map[y, x]
                if biome == 0:
                    z_data[y, x] = 0.0
                    colour_data[y, x] = colours[0]
                elif biome == 1:
                    z_data[y, x] = 0.0
                    colour_data[y, x] = colours[1]
                elif biome == 2:
                    z_data[y, x] = 1.0
                    colour_data[y, x] = colours[2]
                elif biome == 3:
                    z_data[y, x] = 1.0
                    colour_data[y, x] = colours[3]

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    X, Y = np.meshgrid(np.arange(width_grid), np.arange(height_grid))

    ax.plot_surface(X, Y, z_data, facecolors=colour_data, shade=False, rstride=1, cstride=1, linewidth=0, antialiased=False)
    ax.set_title("3d Visualization of Coral Reef Ecosystem")

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    ax.view_init(elev=50, azim=-45)

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

    gen_0 = generate_coral_placement(my_biomes, seed=42)
    rng = np.random.default_rng(seed=999)

    history = [gen_0]
    current_state = gen_0.copy()

    for generation in range(1, 11):
        current_state = simulate_generation(my_biomes, current_state, rng)
        
        history.append(current_state.copy())

    plot_evolution(my_biomes, history)

    plot_3d_map(my_biomes, my_corals)