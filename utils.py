import math
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from cdlib import viz, algorithms
from cdlib.classes import NodeClustering
from stock_graph_creation import correlation_to_graph
import numpy as np


def compute_centralities_over_time(df, windows, threshold=0.7):
    metrics = []

    for start, end in windows:
        df_window = df.loc[start:end]
        if df_window.isnull().all().all():
            continue

        corr_matrix = df_window.corr()
        G = correlation_to_graph(corr_matrix, None, threshold=threshold)

        if G.number_of_edges() == 0:
            continue

        n = G.number_of_nodes()
        m = G.number_of_edges()

        metrics.append({
            "Date": end,
            "Density": nx.density(G),
            "Avg_Degree": 2 * m / n,
            "Clustering": nx.average_clustering(G),
            "Num_Components": nx.number_connected_components(G),
            "Largest_Component_Size": max(len(c) for c in nx.connected_components(G))
        })

    return pd.DataFrame(metrics)

def compute_degree_centrality(df_prices, weekly_dates, threshold=0.5):
    degree_centralities = []

    for date in weekly_dates:
        # Intervallo settimanale
        end_date = pd.to_datetime(date)
        start_date = end_date - pd.Timedelta(days=6)
        
        # Slice dei prezzi settimanali
        week_data = df_prices.loc[start_date:end_date].dropna(axis=1, how='any')
        
        if week_data.shape[0] < 2:
            degree_centralities.append(np.nan)
            continue
        
        # Matrice di correlazione
        corr_matrix = week_data.corr()

        # Costruzione grafo
        G = nx.Graph()
        for i in corr_matrix.columns:
            for j in corr_matrix.columns:
                if i != j and corr_matrix.loc[i, j] > threshold:
                    G.add_edge(i, j, weight=corr_matrix.loc[i, j])
        
        # Calcolo degree centrality
        if len(G.nodes) == 0:
            degree_centralities.append(0)
        else:
            centrality_dict = nx.degree_centrality(G)
            avg_centrality = np.mean(list(centrality_dict.values()))
            degree_centralities.append(avg_centrality)

    return degree_centralities


def info(G):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max(k for _, k in G.degree())))
  
  C = sorted(nx.connected_components(G), key = len, reverse = True)

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * len(C[0]) / n, len(C)))

  if isinstance(G, nx.MultiGraph):
    G = nx.Graph(G)

  print("{:>12s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
  print()
  
  return G

def rolling_time_windows(start_date, end_date, window_size_days=15, step_days=7):
    """
    Generate rolling date windows.

    Returns:
    - list of (start_date_str, end_date_str) tuples
    """
    dates = pd.date_range(start=start_date, end=end_date, freq=f"{step_days}D")
    windows = []
    for d in dates:
        end = d + pd.Timedelta(days=window_size_days)
        if end > pd.to_datetime(end_date):
            break
        windows.append((str(d.date()), str(end.date())))
    return windows


def plot_centrality(df, centrality_type='Betweenness', top_k=5):
    """
    Plot centrality over time for top-k stocks by average centrality.
    """
    avg = df.groupby("Stock")[centrality_type].mean()
    top_stocks = avg.sort_values(ascending=False).head(top_k).index

    df_top = df[df["Stock"].isin(top_stocks)]
    pivot = df_top.pivot(index="Date", columns="Stock", values=centrality_type)
    pivot.index = pd.to_datetime(pivot.index)

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=pivot)
    plt.title(f"{centrality_type} Centrality Over Time (Top {top_k})")
    plt.xlabel("Date")
    plt.ylabel(centrality_type)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
