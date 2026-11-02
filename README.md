# Slingshot

**A 3D gravitational slingshot simulation built with Python.**

Slingshot is a physics-based project that explores how gravity can change the trajectory and speed of a spacecraft passing near a planet.

The project uses Newtonian mechanics and numerical integration to simulate the motion of celestial bodies and a spacecraft in space.

## Project Preview

Screenshots and a demonstration video will be added as the visual side of the project develops.

## The Idea

A gravitational slingshot, also called a gravity assist, happens when a spacecraft passes close to a moving planet.

The planet's gravity changes the spacecraft's velocity. Under the right conditions, the spacecraft can leave the encounter moving faster relative to the Sun.

The goal of Slingshot is to simulate and visualize this process in three dimensions.

## Physics Behind the Simulation

The simulation is based on Newtonian mechanics.

The main concepts include:

- **Newton's Law of Universal Gravitation:** describes the gravitational attraction between two masses.
- **Newton's Second Law:** relates force, mass and acceleration.
- **Velocity and Position:** describe how objects move through space.
- **Numerical Integration:** calculates how the system changes over time.

The gravitational force between two objects is:

\[
F = G\frac{m_1m_2}{r^2}
\]

The project uses the Fourth-Order Runge-Kutta method (RK4) to calculate the evolution of the system over time.

## Current Features

- Gravitational interaction between a Sun and a planet.
- Three-dimensional position and velocity calculations.
- A spacecraft influenced by the gravity of both bodies.
- RK4 numerical integration.
- Visualization of celestial bodies and their trajectories.
- A fixed physics timestep with adjustable simulation speed.

The spacecraft is currently treated as a test particle. This means it experiences gravitational forces from the Sun and planet but does not affect their motion.

## Technology

- **Python:** main programming language.
- **NumPy:** vector and mathematical calculations.
- **Ursina Engine:** 3D visualization.
- **Pytest:** testing and validation.

## Project Structure

```text
src/
└── slingshot/
    ├── main.py
    ├── physics/
    │   ├── gravity.py
    │   └── energy.py
    ├── simulation/
    │   ├── integrator.py
    │   └── system.py
    └── visuals/

tests/
├── test_gravity.py
└── test_energy.py
```

### Main Modules

- `physics/`: contains gravitational calculations and energy calculations.
- `simulation/`: contains the numerical integrator and simulation logic.
- `visuals/`: contains the 3D visualization components.
- `main.py`: brings the simulation and visual components together.

## Installation

Clone the repository:

```bash
git clone https://github.com/stephanetchatchum/3D_Slingshot_Game
cd 3D_Slingshot_Game
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
source .venv/Scripts/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Install the project:

```bash
pip install -e .
```

## Running the Simulation

```bash
python -m slingshot.main
```

## Running Tests

```bash
python -m pytest
```

## Development Roadmap

- [x] Implement gravitational interactions between the Sun and planet.
- [x] Implement RK4 numerical integration.
- [x] Add spacecraft gravitational acceleration.
- [x] Include the spacecraft in the simulation.
- [ ] Build a complete gravitational slingshot demonstration.
- [ ] Add collision detection.
- [ ] Improve 3D celestial body models and space environment.
- [ ] Add spacecraft models and improved trajectory visualization.
- [ ] Add simulation controls and a data interface.
- [ ] Measure and visualize spacecraft speed before and after a flyby.

## Project Goal

The long-term goal is to create an interactive three-dimensional simulation that demonstrates gravitational assists while making the underlying physics and numerical methods understandable.

This project is also an opportunity to explore computational physics, numerical methods and scientific visualization.

## License

MIT License. See the `LICENSE` file for details.