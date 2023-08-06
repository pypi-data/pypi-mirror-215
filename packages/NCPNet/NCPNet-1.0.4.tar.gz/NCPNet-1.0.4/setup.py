from setuptools import setup, find_packages
from pathlib import Path
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='NCPNet',
    version='1.0.4',
    author='Guojia Wan',
    author_email='guojiawan@whu.edu.cn',
    description='Learning synapse-level brain circuit networks. Include training, inferring, evaluation, and visualization.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/mxz12119/NCPNet',
    packages=find_packages(),
    setup_requires=['torch>=2.0.1'],
    install_requires=[
        'torch_geometric>=2.3.1',
        'torch-cluster>=1.6.1',
        'torch-sparse>=0.6.17',
        'torch-scatter>=2.1.1',
        'navis==1.4.0',
        'neuprint-python==0.4.25',
        'networkx',
        'tqdm',
        'tensorboardx',
        'pandas',
        'numpy',
        'scikit-learn',
        'zmq',
        'pyyaml'
    ],
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)