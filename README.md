# 📦 Dynamic-Package-Vehicle-Assignment-Routing-System

## Overview

This project is developed for the **ENCS3340 - Artificial Intelligence** course at Birzeit University, 2nd Semester 2024/2025. It simulates and optimizes the operations of a local package delivery service using AI-based search algorithms to reduce costs and improve efficiency.

---

## 🚀 Features

- **Simulated Annealing (SA)** and **Genetic Algorithm (GA)** implementations.
- Interactive **GUI** to define and visualize delivery routes.
- Configurable number of delivery vehicles and their capacities.
- Constraint-aware assignment of packages based on weight and priority.
- Dynamic **route animation** and performance feedback.
- Error handling for infeasible scenarios (e.g., overloaded or unassignable packages).

---

## 🧠 Problem Formulation

Each package is defined by:
- Destination coordinates `(x, y)`
- Weight in kilograms
- Delivery priority (1 = highest, 5 = lowest)

Each vehicle has:
- A maximum carrying capacity (in kg)
- A starting point at the central depot `(0, 0)`

### Objective
- **Minimize total travel distance**
- Prefer delivering **high-priority packages earlier**
- Ensure **valid assignments** under capacity constraints

---

## ⚙️ How It Works

### Algorithms Implemented

#### 🧬 Genetic Algorithm (GA)
- Population of possible solutions (chromosomes)
- **Selection**, **crossover**, and **mutation** operations

#### 🔥 Simulated Annealing (SA)
- Starts from a greedy solution
- Probabilistic exploration of neighbors


Users can choose either algorithm at runtime.


