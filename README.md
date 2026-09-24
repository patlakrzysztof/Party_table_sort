# Seating Optimizer

**author: Krzysztof Patla**

A graphical user interface (GUI) application used to automatically optimize guest seating at tables. It uses a Simulated Annealing algorithm to assign guests to seats in a way that maximizes positive relationships and minimizes conflicts between guests.

## Requirements

To run the application, you need Python 3.13 and the PySide6 library for the graphical interface.

```bash
pip install PySide6
```

## Running the application

To start the application, execute the main program file in your terminal:

```bash
python main.py
```

## Main features

- **Guest management:** Add and remove individual guests from the list.
- **Couples:** Create pairs (e.g. married couples or partners) that the algorithm will always seat at the same table (treating them as a single, inseparable element with the best relationship).
- **Table configuration:** Define number of tables and their capacities.
- **Relations matrix:** Determine the sympathy/antipathy between individual guests on a scale from **-99 to 99**. These values drive the optimization algorithm.
- **Maximum iterations configuration:** Set the maximum number of iterations according to your needs.
- **State management (Presets):** Save and load entered data (guests, couples, relations, tables, iterations) to JSON files.
- **Result export:** Generate the best-found seating arrangement with the option to save it to a `.txt` file.

## How to use

1. **Guests:** Enter the first and last name in the text field and click "Add" (To remove guest you will need to click on the name and click "Remove" button).
2. **Couples:** Select two people from the dropdown lists and click "Add". They will no longer be treated as "Singles" and will be paired (You can remove the couple and the partners become singles again ).
3. **Tables:** Enter the table capacity (Capacity) and count (Count), then add them to the pool.
4. **Relations:** Select a person from the dropdown list in the right panel. In the table below, assign their relations with other guests (from -99 to 99 and there is one value for both people in relation). Empty fields or invalid values are ignored. Couples have their relation locked at 100 by default.
5. **Algorithm settings:** Enter the number of iterations (100 by default). The higher the value, the longer the algorithm will search for a perfect solution, but the chances of finding an optimal result increase.
6. **Calculate:** Click "Find best solution". The result will appear in the bottom "Output" window, showing the total score of the seating arrangement and the list of people assigned to specific tables.

## File structure

- `main.py` – Handles the graphical user interface (GUI) built with PySide6, manages data entry, and integrates with the algorithm.
- `optimiser.py` – The `SeatingOptimizer` class containing the core logic that solves the problem using the simulated annealing algorithm.
- `exceptions.py` – A collection of custom exceptions used by the optimizer to handle invalid moves (e.g., lack of seats, element not at table).
