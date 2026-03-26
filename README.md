# Path Finding Agent: AI Search Algorithm Visualizer

An interactive Python application that visualizes how different AI agents find the shortest path between two points in a 2D grid. The project compares the efficiency, path length, and exploration patterns of three fundamental search algorithms.

## Features
* **Interactive Grid:** A $15 \times 15$ grid where users can visualize real-time pathfinding.
* **Algorithm Comparison:** Implements and compares:
  * **BFS (Breadth-First Search):** Guarantees the shortest path.
  * **DFS (Depth-First Search):** Explores deep but may find sub-optimal paths.
  * **A* Search:** Uses heuristics to find the optimal path efficiently.
* **Visual Feedback:** Neon-coded GUI highlighting the start (Green), goal (Red), explored cells (Violet), and the final path (Blue).

## Project Structure
* **`main.py`**: The entry point for the Pygame application and animation logic.
* **`algorithms.py`**: Core implementations of BFS, DFS, and A* using `heapq` and `deque`.
* **`grid_gui.py`**: Handles the graphical rendering and color prioritization.
* **`grid.py`**: Manages the underlying $15 \times 15$ matrix structure.
* **`Report.pdf`**: Detailed academic analysis of algorithm performance and search patterns.

## Installation & Usage
1. **Requirements:**
   * Python 3.x
   * Pygame
2. **Run the application:**
   ```bash
   python main.py