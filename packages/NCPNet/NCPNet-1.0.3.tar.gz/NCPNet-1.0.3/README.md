# NCPNet
![PyPI](https://img.shields.io/pypi/v/NCPNet)![Packagist License](https://img.shields.io/packagist/l/mxz12119/NCPNet)


## 1. Brief Introduction
Neuronal Circuit Prediction Network (NCPNet), a simple and effective model for inferring neuron-level connections in a brain circuit network.
## 2. Installation
### Requirements
* Linux
* CUDA environment >=10.2
* NVIDIA CUDA Compiler Driver NVCC version>=10.2. This is used for compiling the dependencies of torch_geometric: torch-cluster,torch-sparse,torch-scatter.
* torch==1.8.0

### Step 1
1. Ensure that [nvcc](https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html) is accessible from terminal and version >=10.2

```nvcc --version```

If NVCC is not not included in your device,  it can be installed through the CUDA Toolkit. NVCC is a part of the [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads?target_os=Linux).

2. Ensure that CUDA is usable and version >=10.2
```
nvidia-smi |grep Version
>>>CUDA Version: >=10.2
```
### Step 2
Use pip to install NCPNet
```
pip install NCPNet
```
Note that it takes a long time to build torch-cluster,torch-sparse,and torch-scatter by pip. Don`t worry, just wait for a while.
### Our main dependencies:
```
torch==1.8.0
torch_geometric==2.0.1
torch-cluster==1.5.9
torch-sparse==0.6.12
torch-scatter==2.0.8
navis==1.3.1
neuprint-python==0.4.25
```
If you would like to reproduce our experiments and plots, please also install jupyter.
```
pip install jupyter
```

## Code structure:
```
Source Code
├── data
|   ├──Hemibrain
|   └──C.Elegans
├── example
├── runs
├── configs
├── NCPNet
|   ├── approaches
|   ├── brain_data.py
|   ├── task.py
|   ├── trainer.py
|   └── utils.py
└── requirements.txt
```
## Examples
### 1. Easy train a model on *Drosophila* HemiBrain
NCPNet uses a configuration file (yaml) to control training and test.

Run 
```
python main_run.py -c configs/linkpred.yaml
```
linkpred.yaml include the hyperparameters of NCPNet.
### 2. Predict  neuronal connection
 Once you train a model, such as 'model.ncpnet', then use the following command to predict the probility between two neurons:
 ```
 python -m NCPNet -pred 1721996278 1722670151 -m model.ncpnet
 ```
 Response:
 ```
 Inferring the connection probability of (1721996278->1722670151)
The score of (1721996278->1722670151): 0.874
 ```
## Reproducibility of Our Paper
Please try to use jupyter to reproduce our experiments in ./examples/

## Access Data
### Raw Data
The *Drosophila* connectome is available at <https://www.janelia.org/project-team/flyem/hemibrain>.


The *C.elegans* connectome is available at <https://wormwiring.org/>
### Preprocessed Data
The data will be released after the review process.







