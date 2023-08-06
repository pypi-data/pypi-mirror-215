from setuptools import setup, find_packages

setup(
    name='pipeline_viz',
    version='0.1.0',
    url='https://github.com/<Your-GitHub-Username>/pipeline_viz',
    author='Author Name',
    author_email='author@gmail.com',
    description='Visualization tools for sklearn pipelines',
    packages=find_packages(),    
    install_requires=['numpy', 'matplotlib', 'networkx', 'plotly', 'scikit-learn'],
)
