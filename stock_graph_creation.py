import yfinance
import pandas as pd
import networkx as nx


def get_sp500_stocks(start_date, end_date):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    table = tables[0]
    stocks = list(table["Symbol"])
    dataset = yfinance.download(stocks, start=start_date, end=end_date)
    df_filtered = dataset["Close"] / dataset["Open"]
    return df_filtered

def correlation_to_graph(corr_matrix: pd.DataFrame, threshold: float = 0.7) -> nx.Graph:
    """
    Create a graph from a correlation matrix.
    
    Parameters:
    - corr_matrix: A pandas DataFrame representing the correlation matrix (stocks × stocks).
    - threshold: Minimum absolute correlation value to include an edge.

    Returns:
    - G: A networkx.Graph object with nodes and weighted edges.
    """
    G = nx.Graph()
    G.name = "correlations"
    
    # Add nodes (stock tickers)
    for i, stock in enumerate(corr_matrix.columns):
        G.add_node(i, label=stock)

    # Add edges for correlations above threshold
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]

            if abs(corr_value) >= threshold:
                G.add_edge(i, j, weight=corr_value)

    return G

def correlation_to_pos_neg_graphs(corr_matrix: pd.DataFrame, threshold: float = 0.7):
    """
    one graph with strong positive correlation edges and another with strong negative correlation edges
    """
    G_pos = nx.Graph()
    G_pos.name = "pos_correlations"
    G_neg = nx.Graph()
    G_neg.name = "neg_correlations"

    for i, stock in enumerate(corr_matrix.columns):
        G_pos.add_node(i, label=stock)
        G_neg.add_node(i, label=stock)

    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_value = corr_matrix.iloc[i, j]

            if corr_value >= threshold:
                G_pos.add_edge(i, j, weight=corr_value)
            elif corr_value <= -threshold:
                G_neg.add_edge(i, j, weight=abs(corr_value))  # keep weight positive for easier handling

    return G_pos, G_neg
