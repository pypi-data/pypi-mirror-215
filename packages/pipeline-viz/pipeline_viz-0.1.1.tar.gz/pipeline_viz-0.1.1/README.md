# visualize_pipeline
A Python package that provides a convenient way to visualize Scikit-learn machine learning pipelines. It utilizes libraries such as NetworkX, Matplotlib, and Plotly to generate clear, interactive, and insightful visual representations of your ML pipelines

## Installation

You can install Visualize Pipeline using pip:

```python
pip install visualize-pipeline

```
## Dependencies

Visualize Pipeline depends on the following Python libraries:

--NetworkX
--Matplotlib
--Plotly
--Scikit-Learn

### You can install these dependencies using pip:
```python
pip install networkx matplotlib plotly scikit-learn

```
## Usage

### Basic Example
Here's a basic example of how to use Visualize Pipeline:

```python
from visualize_pipeline import visualize_pipeline
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Create a simple pipeline
pipe = Pipeline([
    ('scale', StandardScaler()),
    ('clf', LogisticRegression())
])

# Visualize the pipeline
graph = visualize_pipeline(pipe)

# Save the graph to an HTML file
convert_graph_to_plot(graph, 'pipeline.html')

```

This will create an interactive HTML file pipeline.html with the visualization of your pipeline.

### Example in Google Colab with a complex pipeline

```python
pipe = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), [0, 1]),
        ('cat', OneHotEncoder(), [2, 3])])

complex_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', pipe)])

graph = visualize_pipeline(complex_pipeline)
# fig = convert_graph_to_plot(graph)

# Convert the graph to a plotly figure
fig = convert_graph_to_plot(graph, filename='pipeline.html')
from IPython.display import HTML

# Display the HTML file
display(HTML('pipeline.html'))

```

### Visual Example

![Pipeline Visualization Example 1](https://raw.githubusercontent.com/pritiyadav888/visualize_pipeline/main/images/Screenshot%202023-06-21%20at%2010.22.21%20PM.png)

![Pipeline Visualization Example 2](https://raw.githubusercontent.com/pritiyadav888/visualize_pipeline/main/images/Screenshot%202023-06-21%20at%2010.22.27%20PM.png)


## Scope

Visualize Pipeline currently supports Scikit-Learn's Pipeline, FeatureUnion, and ColumnTransformer classes. It can visualize pipelines with nested pipelines and feature unions/column transformers.

The package is meant for visualizing the structure of your pipelines and does not show the actual data flow or transformations in the pipeline.

### Contributing
Contributions are welcome! Please open an issue or submit a pull request on the GitHub repository.

