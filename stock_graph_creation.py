import yfinance
import pandas as pd
import networkx as nx


def get_sp500_stocks(start_date, end_date):
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    table = tables[0]
    stocks = list(table["Symbol"])
    dataset = yfinance.download(stocks, start=start_date, end=end_date)
    df_filtered = dataset["Close"]
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
    
    # Add nodes (stock tickers)
    for stock in corr_matrix.columns:
        G.add_node(stock)

    # Add edges for correlations above threshold
    for i, stock1 in enumerate(corr_matrix.columns):
        for j in range(i + 1, len(corr_matrix.columns)):
            stock2 = corr_matrix.columns[j]
            corr_value = corr_matrix.iloc[i, j]

            if abs(corr_value) >= threshold:
                G.add_edge(stock1, stock2, weight=corr_value)

    return G
