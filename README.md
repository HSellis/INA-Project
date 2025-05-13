# INA-Project

"Stock Correlation Networks: A Network Analysis of the Financial Market"

   
Project Goals

- Build a correlation-based network of stocks using daily returns (yfinance).

- Analyze network structure: communities, centrality, degree distributions, etc.

- Observe temporal changes in the network across different time periods(Optional, if we have time).


Phase 1: Static Network (Main focus – ~7–10 days)
Select 20–50 stocks (e.g., S&P500 top companies or a mix of sectors)

Download historical price data using yfinance
or https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs

Build and analyze the network with:

Community detection (Louvain, Girvan–Newman)

Centrality metrics (degree, betweenness, closeness)

Clustering coefficient, connected components, etc.

Visualize:

Correlation heatmap

Network graph (color-coded by community)


Phase 2: Simple Temporal Analysis (Optional – ~5 days)
Choose 2–3 time windows (e.g., Q1, Q2, Q3 of 2023)

Build a separate network for each period

Compare:

Community structure evolution

Changes in centrality rankings

Interpretation of financial events
