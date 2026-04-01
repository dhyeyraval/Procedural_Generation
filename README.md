# AI-Driven Map Generation: Evolving Coral Ecosystem

This repository contains the entry task for the **AI-Driven Dynamic Procedural Map Generation System** project.

This script implements a multi-layered, deterministic procedural generation system that simulates a living, evolving marine ecosystem. It uses multiple passes of Perlin noise to create environmental conditions (biomes) and applies lightweight Cellular Automata (AI rules) to simulate coral clustering, growth, and decay over time.

## Core Methodology

The system generates the environment and simulates evolution through the following 5-step pipeline:

1.  **Topography Map (Depth):** Uses Perlin noise to generate the physical seabed, thresholded into *Deep Water* and *Shallow Rock*.
2.  **Current Map (Flow):** Uses a secondary Perlin noise generator (different seed/scale) to simulate water currents, thresholded into *Calm Water* and *Strong Current*.
3.  **Biome Matrix:** Combines the two maps to create four distinct ecological zones (e.g., *Exposed Reef* = Shallow Rock + Strong Current).
4.  **Intelligent Placement (Gen 0):** Deterministically seeds "Parent" coral polyps onto valid biomes (Staghorn Corals exclusively on Exposed Reefs, Brain Corals on Sheltered Rocks) and simulates initial clustering.
5.  **Ecosystem Evolution (Cellular Automata):** Runs a time-stepped simulation where corals grow into valid neighboring tiles or die from overcrowding (decay), creating a dynamically shifting ecosystem.

## Installation and Usage

### Requirements

Before executing the script, you will need to install python.
Install the required dependencies using:

```bash
pip install -r requirements.txt
```

### Running the Script

Simply execute the main Python script. The simulation is entirely deterministic; using the default seed guarantees the exact same multi-generation output across all devices.

```bash
python main.py
```

## Configurable Parameters

The system is highly modular. The following parameters control the generation and can be tweaked in the script:

**Environment Parameters:**

  * `width` / `height` (default: `32x32`): The dimensions of the generated grid.
  * `terrain_scale` (default: `10.0`): The zoom level of the depth noise. Lower values create more jagged, chaotic rocks; higher values create broad, smooth shelves.
  * `current_scale` (default: `20.0`): The zoom level of the flow noise. Set higher to create wide, sweeping current channels.
  * `base_seed` (default: `42`): The master seed. Guarantees 100% reproducibility of the terrain, current, and initial coral spawning locations.
  * `octaves` (default: `1`): The number of noise detail layers combined to form the maps. A value of `1` produces clean, smooth biome boundaries ideal for testing, while higher values(e.g., `3` or `4`) layer in finer high-frequency details to create craggy, highly naturalistic rock formations and jagged reef edges.

**AI & Simulation Parameters:**

  * `spawn_attempts` (default: `20`): How many initial coral seeds the AI attempts to place during Generation 0.
  * `cluster_size` (default: `2`): The number of immediate growth iterations applied to the initial seeds before the main timeline begins.
  * **Growth Probabilities:** Staghorn has a `40%` chance to spread to an adjacent valid tile per tick (fast-growing), while Brain Coral has a `20%` chance (slow-growing).
  * **Decay Rule:** If a coral is surrounded by 3 or more neighboring corals, it has a `5%` chance to die from nutrient starvation, freeing up space and ensuring dynamic movement.

## Sample Outputs

The script executes the full generation pipeline sequentially, producing six distinct visual outputs. This allows you to inspect the mathematical logic and AI rules at every stage of the ecosystem's creation:

1. **Step 1: Base Terrain (Depth) - `step1_terrain.png`** Visualizes the primary Perlin noise layer, establishing the physical seabed (Deep Water vs. Shallow Rock).
<p align="center">
  <img src="step1_terrain.png" width="250"/>
</p>

2. **Step 2: Water Current (Flow) - `step2_current.png`** Visualizes the secondary, larger-scale noise layer simulating water flow independently of the seabed.
<p align="center">
  <img src="step2_current.png" width="250"/>
</p>


3. **Step 3: Biome Matrix - `step3_biomes.png`** The mathematical intersection of the Depth and Flow maps, creating four distinct ecological zones.
<p align="center">
  <img src="step3_biomes.png" width="250"/>
</p>


4. **Step 4: AI Coral Placement - `step4_ecosystem.png`** Shows "Generation 0," where coral polyps are deterministically seeded into their required biomes and form initial clusters.
<p align="center">
  <img src="step4_ecosystem.png" width="250"/>
</p>


5. **Step 5: Ecosystem Evolution - `step5_evolution.png`** A side-by-side timeline (Gen 0 to Gen 10) demonstrating the Cellular Automata simulation. Corals organically grow into valid adjacent space or decay from overcrowding.
![Demo Image](step5_evolution.png)



### Color Legend (For Steps 3 through 6):
* **Dark Blue:** Deep Calm Water
* **Teal:** Deep Flowing Current
* **Beige:** Sheltered Rock
* **Orange:** Exposed Reef (Strong current over shallow rock)
* **Magenta:** Staghorn Coral (Requires Exposed Reef)
* **Bright Green:** Brain Coral (Requires Sheltered Rock)

## Step 6: 3D Topographical Visualization

To bridge the gap between 2D data matrices and the 3D environments required for the mARine AR application, the script includes a final 3D rendering function (`step6_3d_map.png`).

Using `matplotlib`, the initial generation (Gen 0) of the simulated ecosystem is extruded into a 3D topographical map. This demonstrates exactly how flat, procedural biome data translates into rendering instructions for a game engine like Unity:

* **The X and Y axes** represent the spatial coordinate grid.
* **The Z axis** applies vertical height rules based on the simulation data (Deep Water = `Z:0`, Rock/Reef = `Z:1`, Coral Clusters = `Z:2`).

<p align="center">
  <img src="step6_3d_map.png" width="250"/>
</p>

---