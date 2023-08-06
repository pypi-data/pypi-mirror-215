# Import necessary modules
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.compose import ColumnTransformer
from pipeline_viz import visualize_pipeline, convert_graph_to_plot
import webbrowser
import os
import sys
sys.path.insert(0, './pipeline_viz')

# Create a simple pipeline
pipe = Pipeline(steps=[
    ('scaler', StandardScaler()),
    ('classifier', LogisticRegression())
])

# Create a preprocessor with column transformations
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), [0, 1]),
        ('cat', OneHotEncoder(), [2, 3])
    ])

# Create a complex pipeline using the preprocessor and the simple pipeline
complex_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', pipe)
])

# Visualize the complex pipeline
graph = visualize_pipeline(complex_pipeline)

# Convert the graph to a plot and save it as 'pipeline.html'
fig = convert_graph_to_plot(graph, filename='pipeline.html')

# Open 'pipeline.html' in the default web browser
webbrowser.open('file://' + os.path.realpath('pipeline.html'))
