# Graph Dominant Set Calculation and Online Trading Algorithm

## Overview

This project involves two main components:

1. **Dominant Set Calculation**: This part of the project reads graphs, computes two dominant sets (D1 and D2) for each graph, and stores the results in an output directory. The dominant sets are calculated based on a greedy algorithm and some heuristic strategies.
2. **Online Trading Algorithm**: A function for trading stocks based on certain rules and parameters. It implements a strategy that makes decisions whether to buy, sell, or hold based on the current stock price and a series of constraints such as `max_trade_bound` and `longueur` (duration).

## Project Structure

```bash
.
├── dominant_set.py           # Script for calculating dominant sets from graphs
├── trading_algorithm.py      # Script for implementing the online trading algorithm
├── README.md                 # This file
## Dominant Set Calculation

### Dependencies
- `networkx` library for graph manipulations.
- Python 3.x for running the script.

## Dominant Sets
### Key Functions
- `load_graph(name)`: Loads a graph from a file. The file should contain nodes and edges in a specific format.
- `calculate_score(D1, D2, g)`: Calculates a score based on the intersection of nodes in sets D1 and D2.
- `is_dominant_set(g, d)`: Verifies if a set of nodes `d` is a dominant set in graph `g`.
- `dominant(g)`: Computes the dominant sets D1 and D2 using a mix of greedy algorithms and the longest path heuristic.

## Online Trading Algorithm
### Key Functions
- `achat(taux, taux_achat, trades_done, max_trade_bound, sol_online)`: Buys stocks by setting the purchase rate and updating the transaction count.
- `vente(taux, taux_achat, trades_done, sol_online)`: Sells stocks, closes the transaction, and updates the capital.
- `two_way_trading_online(m, M, longueur, sol_online, day, trades_done, max_trade_bound, taux_achat, taux)`: Implements the online trading algorithm, making buy/sell decisions based on stock prices, trading limits, and other parameters.

### How to Run
To run the dominant set calculation:

1. Prepare a directory containing graph files in the specified format.
2. Execute the script using the following command:

   ```bash
   python dominant_set.py <input_dir> <output_dir>
<input_dir>: Path to the directory containing the input graph files.
<output_dir>: Path to the directory where the results will be saved.
