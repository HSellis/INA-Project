import math
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from cdlib import viz, algorithms
from cdlib.classes import NodeClustering
from stock_graph_creation import correlation_to_graph


def compute_centralities_over_time(df, windows, threshold=0.7):
    """
    Computes centralities for each time window using correlation graphs.
    """
    results = []

    for start, end in windows:
        df_window = df.loc[start:end]
        if df_window.isnull().all().all():
            continue  # skip empty windows

        corr_matrix = df_window.corr()
        G = correlation_to_graph(corr_matrix, threshold=threshold)

        # Skip graphs with no edges (empty graphs)
        if G.number_of_edges() == 0:
            continue

        degree_centrality = nx.degree_centrality(G)
        betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
        closeness_centrality = nx.closeness_centrality(G)

        for stock in G.nodes:
            results.append({
                "Date": end, 
                "Stock": stock,
                "Degree": degree_centrality.get(stock, 0),
                "Betweenness": betweenness_centrality.get(stock, 0),
                "Closeness": closeness_centrality.get(stock, 0)
            })

    return pd.DataFrame(results)


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
