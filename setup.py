from setuptools import setup, find_packages

setup(
    name='layer-centrality',
    version='0.1.0',
    packages=find_packages(),
    url='',
    license='Apache 2.0',
    author='Victor',
    author_email='victor199704@gmail.com',
    description='A package used for computing layer centrality in multilayered networks.',
    install_requires=[
        "cycler==0.12.1",
        "fonttools==4.44.0",
        "joblib==1.3.2",
        "kiwisolver==1.4.5",
        "layer-centrality==0.1.0",
        "matplotlib==3.5.3",
        "networkx==2.6.3",
        "numpy==1.22.4",
        "packaging==23.2",
        "pandas==1.4.4",
        "Pillow==10.1.0",
        "pyparsing==3.1.1",
        "python-dateutil==2.8.2",
        "pytz==2023.3.post1",
        "scikit-learn==1.0.2",
        "scipy==1.7.3",
        "seaborn==0.11.2",
        "six==1.16.0",
        "threadpoolctl==3.2.0",
        "uunet==1.1.4",
        "XlsxWriter==3.1.9"
    ]
)
