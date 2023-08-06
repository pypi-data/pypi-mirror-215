import unittest
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from pipeline_viz import visualize_pipeline, convert_graph_to_plot

class TestPipelineViz(unittest.TestCase):

    def test_visualize_pipeline(self):
        X, y = make_classification()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        clf = LogisticRegression()

        pipeline = Pipeline([
            ('scaler', scaler),
            ('classifier', clf)
        ])

        graph = visualize_pipeline(pipeline)

        self.assertIsNotNone(graph)

    def test_convert_graph_to_plot(self):
        X, y = make_classification()
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        scaler = StandardScaler()
        clf = LogisticRegression()

        pipeline = Pipeline([
            ('scaler', scaler),
            ('classifier', clf)
        ])

        graph = visualize_pipeline(pipeline)
        fig = convert_graph_to_plot(graph)

        self.assertIsNotNone(fig)

if __name__ == '__main__':
    unittest.main()
