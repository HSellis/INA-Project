
# 📊 INA-Project

### **Stock Correlation Networks: A Network Analysis of the Financial Market**

---

## 🎯 Project Goals

This project applies network analysis methods to the financial market by modeling correlations among stock returns as a network.

*  Build a **correlation-based network** of stocks using daily returns from financial data.
*  Analyze the **network structure**:

  * Community detection
  * Centrality measures
  * Degree distributions
  * Clustering coefficients
*  Optionally, **observe temporal evolution** of the network across different time windows to detect structural changes in the market.

---

###  **Phase 1 – Static Network Analysis** *(Main focus – \~7–10 days)*

####  **Data Collection**

* Select **20–50 stocks**, for example:

  * Top companies from the **S\&P500**
  * Or a diverse mix from different **sectors** (Tech, Healthcare, Finance, etc.)
* Download **historical daily price data** using:

  * [`yfinance`](https://pypi.org/project/yfinance/) (preferred, easy to use)
  * Or from [Kaggle dataset](https://www.kaggle.com/datasets/borismarjanovic/price-volume-data-for-all-us-stocks-etfs)

####  **Network Construction**

* Compute **daily returns** for each stock.
* Construct a **correlation matrix** (Pearson).
* Apply a **threshold** (e.g., `|r| > 0.7`) to define edges.
* Create an **undirected, weighted network**, where:

  * Nodes = stocks
  * Edges = significant correlation between returns

####  **Network Analysis**

* **Community Detection**:

  * Louvain algorithm (modularity optimization)
  * Girvan–Newman (edge betweenness)
* **Centrality Measures**:

  * Degree centrality
  * Betweenness centrality
  * Closeness centrality
* **Other Metrics**:

  * Clustering coefficient
  * Connected components
  * Density, diameter, average path length

####  **Visualization**

* **Heatmap** of the correlation matrix (with `seaborn.heatmap`)
* **Network graph**:

  * Visualized with `networkx` or `plotly`
  * Nodes colored by community
  * Node size proportional to centrality (e.g., degree)

---

###  **Phase 2 – Temporal Network Analysis** *(Optional – \~5 days)*

####  **Temporal Segmentation**

* Choose **2–3 distinct time windows**, e.g.:

  * Q1 2023 (Jan–Mar)
  * Q2 2023 (Apr–Jun)
  * Q3 2023 (Jul–Sep)

####  **Dynamic Comparison**

* Build a separate network for each period using the same method as in Phase 1.
* Analyze and **compare**:

  * Evolution of community structures
  * Changes in centrality rankings (e.g., which stock became more/less central)
  * Shifts in clustering or connectivity

####  **Optional Interpretations**

* Highlight market events that might explain changes:

  * Interest rate decisions
  * Economic reports (inflation, unemployment)
  * Company earnings reports
  * Political or global events

---

##  Tools & Libraries

| Purpose          | Tool                                       |
| ---------------- | ------------------------------------------ |
| Financial data   | `yfinance`, `pandas-datareader`, or Kaggle |
| Data processing  | `pandas`, `numpy`                          |
| Network analysis | `networkx`, `python-louvain`               |
| Visualizations   | `matplotlib`, `seaborn`, `plotly`          |

---

##  Deliverables

* 📄 Jupyter Notebook / Python script with clear sections
* 📊 Visualizations:

  * Correlation heatmaps
  * Static and (optional) temporal network graphs
*  Insights and interpretation of the network structure
*  Optional report or presentation slides

---

##  Project Work
* Henri: Community detection
* Riccardo: Centrality measure + (Time Windows analysis)
* Ondra: Graphlets + visualization
