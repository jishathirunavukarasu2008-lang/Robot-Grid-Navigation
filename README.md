# 🤖 Robot Grid Navigation Using BFS

## 1. Project Overview

This project demonstrates how a robot can navigate a two-dimensional grid using an Artificial Intelligence search algorithm.

The robot starts from an initial position and must reach a destination while avoiding obstacles.

Breadth-First Search (BFS) is used to explore the grid and find the shortest path.

---

## 2. Problem Statement

A robot must find its way from a starting position to a destination on a grid containing obstacles.

The robot can move:

- Up
- Down
- Left
- Right

The robot cannot move through obstacle cells.

---

## 3. AI Problem Formulation

The robot navigation problem is represented as a search problem.

| Component | Description |
|---|---|
| Initial State | Robot's starting position |
| State | Robot's current grid position |
| Actions | Up, Down, Left, Right |
| Transition | Movement to a valid neighbouring cell |
| Obstacles | Blocked cells |
| Goal State | Destination position |
| Goal Test | Check whether robot reached destination |
| Path Cost | Number of movements |
| Search Algorithm | Breadth-First Search |

---

## 4. Algorithm

Breadth-First Search (BFS) explores the grid level by level.

A queue is used to store cells that need to be explored.

The algorithm also maintains:

- Visited cells
- Parent information
- Explored states

The parent information is used to reconstruct the final path.

---

## 5. Features

- Grid-based robot navigation
- Obstacles
- BFS shortest-path search
- No-path detection
- Path reconstruction
- Runtime measurement
- Automated testing
- Experimental evaluation
- Basic graphical interface

---

## 6. Project Structure

```text
Robot-Grid-Navigation
│
├── docs
│   ├── problem_formulation.md
│   ├── bfs_algorithm.md
│   ├── complexity.md
│   ├── results.md
│   └── reflection.md
│
├── src
│   ├── bfs.py
│   ├── main.py
│   ├── experiments.py
│   └── visualizer.py
│
├── tests
│   └── test_bfs.py
│
├── README.md
├── requirements.txt
└── .gitignore