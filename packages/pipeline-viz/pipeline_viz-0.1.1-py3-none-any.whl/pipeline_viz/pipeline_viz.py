import networkx as nx
import matplotlib
import matplotlib.cm as cm
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline, FeatureUnion
from .utils import get_color_map

# Included import statement for LogisticRegression

# Add docstring to function
def visualize_pipeline(pipeline, graph=None, parent_node=None, color_index=0):
    """
    Function to visualize a given sklearn pipeline using networkx

    Parameters:
    pipeline: sklearn.pipeline.Pipeline instance
    graph: networkx.Graph instance
    parent_node: str
    color_index: int

    Returns:
    graph: networkx.Graph instance
    """
    if graph is None:
        graph = nx.DiGraph()

    colors = get_color_map(len(pipeline.steps))

    for i, step in enumerate(pipeline.steps):
        name, estimator = step
        estimator_str = str(estimator).replace('), ', '),<br>').replace(', ', ',<br>')
        
        # Extract and format hyperparameters
        hyperparams = estimator.get_params()
        hyperparams_str = '<br>'.join([f'{k}: {v}' for k, v in hyperparams.items()])
        
        node_type = 'transformer' if isinstance(estimator, (FeatureUnion, ColumnTransformer)) else 'estimator'

        graph.add_node(name, 
                       color=colors[color_index % len(colors)],
                       size=15 if hasattr(estimator, 'transform') or isinstance(estimator, LogisticRegression) else 10,
                       info=f'{estimator_str}<br>Hyperparameters:<br>{hyperparams_str}',
                       node_type=node_type)
        
        if i > 0:
            graph.add_edge(pipeline.steps[i-1][0], name, linestyle='dashed' if hasattr(estimator, 'transform') else 'solid')

        if parent_node is not None:
            graph.add_edge(parent_node, name, linestyle='dashed' if isinstance(estimator, (FeatureUnion, ColumnTransformer)) else 'solid')

        if isinstance(estimator, FeatureUnion):
            for j, (transformer_name, transformer_estimator) in enumerate(estimator.transformer_list):
                if isinstance(transformer_estimator, Pipeline):
                    nested_color_index = (color_index + j + 1) % len(colors)
                    visualize_pipeline(transformer_estimator, graph=graph, parent_node=name, color_index=nested_color_index)
                else:
                    transformer_str = str(transformer_estimator).replace('), ', '),<br>').replace(', ', ',<br>')
                    graph.add_node(transformer_name, 
                                   color=colors[color_index],
                                   size=10,
                                   info=transformer_str,
                                   node_type='transformer')  # Set node_type to 'transformer'
                    graph.add_edge(name, transformer_name, linestyle='dashed')

        if isinstance(estimator, ColumnTransformer):
            for j, (transformer_name, transformer_estimator, _) in enumerate(estimator.transformers):
                if isinstance(transformer_estimator, Pipeline):
                    nested_color_index = (color_index + j + 1) % len(colors)
                    visualize_pipeline(transformer_estimator, graph=graph, parent_node=name, color_index=nested_color_index)
                else:
                    transformer_str = str(transformer_estimator).replace('), ', '),<br>').replace(', ', ',<br>')
                    graph.add_node(transformer_name, 
                                   color=colors[color_index],
                                   size=10,
                                   info=transformer_str,
                                   node_type='transformer')  # Set node_type to 'transformer'
                    graph.add_edge(name, transformer_name, linestyle='dashed')

        if isinstance(estimator, Pipeline):
            visualize_pipeline(estimator, graph=graph, parent_node=name, color_index=color_index)

    return graph


def convert_graph_to_plot(graph, filename=None):
    """
    Function to convert a networkx graph into a plotly plot

    Parameters:
    graph: networkx.Graph instance
    filename: str

    Returns:
    fig: plotly.graph_objects.Figure instance
    """
    pos = nx.kamada_kawai_layout(graph)  # Use Kamada-Kawai layout for improved node placement
    edge_x = []
    edge_y = []
    edge_line = []  # Added a list to store line styles

    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_line.append(graph.edges[edge]['linestyle'])  # Store line style for each edge

    node_x = [pos[node][0] for node in graph.nodes()]
    node_y = [pos[node][1] for node in graph.nodes()]
    node_types = [graph.nodes[node]['node_type'] for node in graph.nodes()]  # Added node types
    node_colors = []
    for node_type in node_types:  # Assign colors based on node types
        if node_type == 'transformer':
            node_colors.append('blue')
        elif node_type == 'estimator':
            node_colors.append('red')
        elif node_type == 'union':
            node_colors.append('green')
        else:
            node_colors.append('yellow')  # Set 'yellow' as the default color

    node_size = [graph.nodes[node]['size'] for node in graph.nodes()]
    node_hovertext = [
        f'<b>{node}</b><br>{graph.nodes[node]["info"]}' 
        for node in graph.nodes()
    ]

    # Generate annotations for arrows
    annotations = []
    for i in range(0, len(edge_x), 3):
        annotations.append(
            dict(
                ax=edge_x[i],
                ay=edge_y[i],
                axref='x',
                ayref='y',
                x=edge_x[i+1],
                y=edge_y[i+1],
                xref='x',
                yref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=2,   # Increased arrowsize
                arrowwidth=2,  # Increased arrowwidth
                arrowcolor='#636363'
            )
        )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color=node_colors,
            size=node_size,
            line=dict(width=2)
        ),
        hovertext=node_hovertext,
        text=list(graph.nodes()),
        textposition="top center"
    )

    # Create legend traces with matching colors
    legend_transformer = go.Scatter(x=[None], y=[None], mode='markers',
                                    marker=dict(size=10, color='blue'),
                                    name='Transformer')
    legend_estimator = go.Scatter(x=[None], y=[None], mode='markers',
                                  marker=dict(size=15, color='red'),
                                  name='Estimator')
    legend_union = go.Scatter(x=[None], y=[None], mode='markers',
                              marker=dict(size=12, color='green'),
                              name='Feature Union / Column Transformer')

    fig = go.Figure(data=[node_trace, legend_transformer, legend_estimator, legend_union],
                    layout=go.Layout(
                        title='Pipeline Visualization',
                        titlefont=dict(size=16),
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    ))

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial"
        ),
        hoverdistance=10,
        spikedistance=10,
        dragmode=False,  # Disable drag mode
        annotations=annotations  # Add annotations here
    )

    if filename:
        pio.write_html(fig, file=filename, auto_open=False)

    return fig