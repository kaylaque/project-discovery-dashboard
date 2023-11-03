import streamlit as st
import networkx as nx
import plotly.graph_objects as go

def main():
    st.title("Network Visualization Example")

    # Create a sample network graph
    G = nx.Graph()
    G.add_node("Node A")
    G.add_node("Node B")
    G.add_edge("Node A", "Node B")

    # Create a Plotly figure from the network graph
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
    )

    # Create the Plotly figure and layout
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                    ))

    # Display the network visualization
    st.plotly_chart(fig)

if __name__ == "__main__":
    main()
