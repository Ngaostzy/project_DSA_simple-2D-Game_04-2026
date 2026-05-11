# Nameless Cat - 2D Platformer Project (DSA 04-2026)

> A 2D indie platformer developed entirely in Python using the Pygame library. This project serves as a practical implementation of fundamental Data Structures, Algorithms (DSA), Kinematics, and Linear Algebra within game logic engineering. The architecture adheres to a strict Object-Oriented Programming (OOP) paradigm and utilizes dynamic spatial data loading via LDtk.

---

## 1. Project Overview

In **Nameless Cat**, the player navigates an avatar through complex environmental hazards and diverse hostile entities to reach a spatial portal. The project minimizes reliance on pre-built physics engines, focusing instead on writing mathematical and algorithmic logic from scratch to handle movement, collision, and artificial intelligence.

---

## 2. Algorithmic & Technical Analysis

The project integrates several foundational computational techniques to govern gameplay mechanics:

### 2.1. Finite State Machine (FSM)
* **Deterministic Game Loop:** Manages the primary application state through discrete, isolated phases (`START_MENU` -> `PLAYING` -> `GAME_OVER` / `LEVEL_COMPLETE`), ensuring optimal resource allocation by freezing updates for inactive states.
* **State-Driven AI:** Hostile entities utilize FSMs for seamless behavioral branching (`walk` -> `chase` -> `attack`), transitioning based on continuous sensory input and proximity heuristics.

### 2.2. Axis-Aligned Bounding Box (AABB) Collision
Processes spatial intersections between rectangular entity bounds. The system implements a "Forgiving Hitbox" mechanism (geometric padding via `pad_x` and `pad_y`) for static hazards such as spikes. This spatial margin reduces the bounding box relative to the visual sprite, minimizing edge-case collision errors and optimizing maneuverability.

### 2.3. Raycasting & Edge Detection
Patrolling entities (`PATROL_ENEMY`) utilize a predictive "virtual sensor" functioning as a short-range raycast ahead of their kinematic trajectory. If the spatial query returns no ground intersection, the AI registers an environmental gap and autonomously inverts its horizontal velocity, preventing unintentional free-fall.

### 2.4. Linear Algebra & Applied Mathematics
* **Vector Normalization:** Applied in ranged combat (`AIMING_ENEMY`). The distance vector between the projectile origin and the target coordinates is normalized and scaled by a predefined constant, ensuring uniform scalar velocity regardless of the target's relative distance.
* **Sinusoidal Kinematics:** Utilizes the `math.sin()` function synchronized with temporal ticks (`pygame.time.get_ticks()`) to simulate harmonic oscillation. This governs the continuous hovering displacement of aerial entities and portal visual effects.
* **AI Hysteresis:** Pursuing entities (`CHASE_ENEMY`) implement dual-threshold line-of-sight metrics (a minimal radius for initial detection and a maximum radius for sustained pursuit). This hysteresis loop effectively prevents behavioral jittering when the player oscillates near the vision boundary.

---

## 3. System Architecture & Inheritance Topology

The entity framework is strictly hierarchical, leveraging OOP inheritance to ensure code modularity and adhere to the DRY (Don't Repeat Yourself) principle.

```text
[ Entity Object Topology ]

   ENTITY (Base Class: Gravity, Velocity, Grid-based Collision Resolution)
     |
     +-- PLAYER (User-controlled kinematics and state handling)
     |
     +-- ENEMY_BASE (Inherits physics, adds player AABB intersection routines)
           |
           +-- PATROL_ENEMY (Oscillating horizontal movement via spatial anchors)
           |     |
           |     +-- CHASE_ENEMY (Integrates line-of-sight heuristics and melee states)
           |
           +-- AIMING_ENEMY (Sinusoidal vertical displacement, vector-based projectiles)
           |
           +-- RANGED_HORIZONTAL (Stationary/Patrol emission with temporal cooldowns)