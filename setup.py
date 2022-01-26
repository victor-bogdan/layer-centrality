from setuptools import setup, find_packages

setup(
    name='layer-centrality',
    version='0.1.0',
    packages=find_packages(),
    url='',
    license='Apache 2.0',
    author='Victor',
    author_email='victor199704@gmail.com',
    description='A package used for computing layer centrality in multilayered networks',
    install_requires=[
        "uunet~=1.1.4",
        "networkx~=2.6.3",
        "matplotlib~=3.5.1",
        "numpy~=1.22.1",
        "seaborn~=0.11.2",
        "pandas~=1.4.0",
        "scikit-learn~=1.0.2",
        "scipy~=1.7.3",
        "setuptools~=57.0.0"
    ]
)
