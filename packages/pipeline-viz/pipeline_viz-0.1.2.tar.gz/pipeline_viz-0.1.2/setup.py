from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pipeline_viz',
    version='0.1.2',
    url='https://github.com/pritiyadav888/visualize_pipeline.git',
    author='Pritii Yadav',
    author_email='pritiyadav888@gmail.com',
    description='Visualization tool for sklearn pipelines',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),    
    install_requires=['numpy', 'matplotlib', 'networkx', 'plotly', 'scikit-learn'],
)
