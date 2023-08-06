from hashlib import new
from typing import Optional, Callable, List

import os.path as osp
import numpy as np
from sklearn import neighbors

import torch
from torch.utils.data import DataLoader,Sampler
import torch_geometric
from torch_geometric.data import InMemoryDataset, download_url
from torch_geometric.io import read_planetoid_data
from torch_geometric.data import Data
from torch_geometric.utils import negative_sampling
import networkx as nx
import random
from NCPNet.utils import edge_index2Graph

class HemiBrain(InMemoryDataset):
    r"""
    Args:
        root (string): Root directory where the dataset should be saved.
        transform (callable, optional): A function/transform that takes in an
            :obj:`torch_geometric.data.Data` object and returns a transformed
            version. The data object will be transformed before every access.
            (default: :obj:`None`)
        pre_transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric.data.Data` object and returns a
            transformed version. The data object will be transformed before
            being saved to disk. (default: :obj:`None`)
    """

    url = 'null'

    def __init__(self, root: str,split='node', transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None,process=False,restore_split=None,device=None):

        super().__init__(root, transform, pre_transform)
        if device is None:
            self.device='cpu'
        else:
            self.device=device
        if process:
            self._process()
        if restore_split is None:
            self._data, self.slices = torch.load(self.processed_paths[0],map_location=self.device)
        elif isinstance(restore_split,str):
            self._data= torch.load(restore_split,map_location=self.device)
        self._data, self.slices = self.collate([self._data])

    @property
    def num_edges(self):
        return self._data.edge_index.size(0)
    @property
    def edge_index(self):
        return self._data.edge_index
    @property
    def y(self):
        return self._data.y
    
    @property
    def num_nodes(self):
        return self._data.num_nodes
    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, 'processed')

    @property
    def raw_file_names(self) -> List[str]:
        return ['edges.txt','edges_ROI.txt','nuron-label.txt','neuron2ID.txt']

    @property
    def processed_file_names(self) -> str:
        return 'data.pt'
    @property
    def neu2ID(self):
        if hasattr(self,'neu2ID_dict'):
            return self.neu2ID_dict
        else:
            neu2ID={}
            with open(osp.join(self.raw_dir,'neuron2ID.txt'),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split(',')
                    neu2ID[line[0]]=int(line[1])
            self.neu2ID_dict=neu2ID
            return self.neu2ID_dict
    @property
    def label2ID(self):
        if hasattr(self,'label2ID_dict'):
            return self.label2ID_dict
        else:
            self.neuron2label_dict={}
            with open(osp.join(self.raw_dir,'neuron-label.txt'),'r') as fin:
                for i in fin.readlines():
                    line = i.strip().split('\t')
                    self.neuron2label_dict[line[0]]=line[1]
            label_set= set(self.neuron2label_dict.values())
            self.label2ID_dict={l:k for k,l in enumerate(label_set)}
            return self.label2ID_dict
    @property
    def neuron2label(self):
        if hasattr(self,'neuron2label_dict'):
            return self.neuron2label_dict
        else:
            self.neuron2label_dict={}
            with open(osp.join(self.raw_dir,'neuron-label.txt'),'r') as fin:
                for i in fin.readlines():
                    line = i.strip().split('\t')
                    self.neuron2label_dict[line[0]]=line[1]
            label_set= set(self.neuron2label_dict.values())
            self.label2ID_dict={l:k for k,l in enumerate(label_set)}
            return self.neuron2label_dict
    @property
    def typedim(self):
        if hasattr(self,'cache_type_dim'):
            return self.cache_type_dim
        else:
            label2ID=self.label2ID
            self.cache_type_dim=len(label2ID.keys())
            return self.cache_type_dim

    @staticmethod
    def read_data(raw_dir):
        neu2ID={}
        with open(osp.join(raw_dir,'neuron2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(',')
                neu2ID[line[0]]=int(line[1])
        ID2neu={v:k for k,v in neu2ID.items()}
        edge_index=[]
        edge_attr=[]
        with open(osp.join(raw_dir,'edges.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(',')
                if len(line)==3:
                    edge_index.append([neu2ID[line[0]],neu2ID[line[1]]])
                    edge_attr.append([int(line[2])])

        edge_index=torch.Tensor(edge_index)
        edge_index=torch.transpose(edge_index,0,1)
        edge_index=edge_index.to(dtype=torch.int64)
        edge_attr=torch.Tensor(edge_attr)
        neuron2label={}
        with open(osp.join(raw_dir,'neuron-label.txt'),'r') as fin:
            for i in fin.readlines():
                line = i.strip().split('\t')
                neuron2label[line[0]]=line[1]
        label_set= set(neuron2label.values())
        label2ID={l:k for k,l in enumerate(label_set)}

        y=[]
        for i_neuron in range(len(ID2neu)):
            label_x=neuron2label[ID2neu[i_neuron]]
            y.append(label2ID[label_x])
        y=torch.tensor(y)

        x=torch.nn.functional.one_hot(y)
        x=x.to(dtype=torch.float32)

        return Data(x=x,edge_index=edge_index,y=y,edge_attr=edge_attr,neu2ID=neu2ID,label2ID=label2ID)

    def process(self):
        data = self.read_data(self.raw_dir)
        data = data if self.pre_transform is None else self.pre_transform(data)
        torch.save(self.collate([data]), self.processed_paths[0])
    def manual_split(self,path):
        label2ID={}
        with open(osp.join(path,'label2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    label2ID[line[0]]=int(line[1])
        neu2ID={}
        with open(osp.join(path,'neu2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    neu2ID[line[0]]=int(line[1])
        
        for k,v in self.neu2ID.items():
            if neu2ID[k]!=v:
                raise ValueError('this file doesn`t match this object(%s)'%__name__)

        test_edge_index=[]
        with open(osp.join(path,'test_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    test_edge_index.append([n1,n2])
        test_edge_index=torch.tensor(test_edge_index).T
        
  
        train_edge_index=[]
        with open(osp.join(path,'train_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    train_edge_index.append([n1,n2])
        train_edge_index=torch.tensor(train_edge_index).T

        total_edges=test_edge_index.size(1)+train_edge_index.size(1)
        if test_edge_index.size(1)>int(total_edges*0.1):
            test_edge_index=test_edge_index[:,:int(total_edges*0.1)]

        test_edge_index=test_edge_index.to(device=self._data.x.device)
        train_edge_index=train_edge_index.to(device=self._data.x.device)


        test_data=Data(x=self._data.x,y=self._data.y,edge_index=test_edge_index,neu2ID=neu2ID,label2ID=label2ID)
        train_data=Data(x=self._data.x,y=self._data.y,edge_index=train_edge_index,neu2ID=neu2ID,label2ID=label2ID)
        return train_data,test_data





    def __repr__(self) -> str:
        return 'HemiBrain'
class Celegans19(InMemoryDataset):
    r"""
    Args:
        root (string): Root directory where the dataset should be saved.
        name (string): The name of the dataset (:obj:`"Male"`,
            :obj:`"Hermaphrodite"`).
        transform (callable, optional): A function/transform that takes in an
            :obj:`torch_geometric.data.Data` object and returns a transformed
            version. The data object will be transformed before every access.
            (default: :obj:`None`)
        pre_transform (callable, optional): A function/transform that takes in
            an :obj:`torch_geometric.data.Data` object and returns a
            transformed version. The data object will be transformed before
            being saved to disk. (default: :obj:`None`)
    """

    url = 'null'

    def __init__(self, root: str,name='male',split='node', transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None,process=False):
        self.name=name
        if name=='male':
            self.data_prefix='MaleWorm'
        elif name=='herm':
            self.data_prefix='HermaphroditeWorm'

        super().__init__(root, transform, pre_transform)
        if process:
            self._process()
        self.data, self.slices = torch.load(self.processed_paths[0])
        self.data, self.slices = self.collate([self.data])

    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, 'processed')

    @property
    def raw_file_names(self) -> List[str]:
        return ['HermaphroditeWorm-cell-type.txt','HermaphroditeWorm-edge_list.txt','MaleWorm-cell-type.txt','MaleWorm-edge_list.txt']

    @property
    def processed_file_names(self) -> str:
        return '%s-data.pt'%self.name
    @property
    def neu2ID(self):
        if hasattr(self,'neu2ID_dict'):
            return self.neu2ID_dict
        else:
            Neuron2Type={}
            with open(osp.join(self.raw_dir,'%s-cell-type.txt'%(self.data_prefix)),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split('\t')
                    if len(line)==2:
                        Neuron2Type[line[0]]=line[1]
            self.neuron2label_dict=Neuron2Type
            Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
            self.neu2ID_dict=Neuron2ID
            type_set=set(Neuron2Type.values())
            Type2id={k:v for v,k in enumerate(type_set)}
            self.label2ID_dict=Type2id
        return self.neu2ID_dict
    @property
    def label2ID(self):
        if hasattr(self,'label2ID_dict'):
            return self.neu2ID_dict
        else:
            Neuron2Type={}
            with open(osp.join(self.raw_dir,'%s-cell-type.txt'%(self.data_prefix)),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split('\t')
                    if len(line)==2:
                        Neuron2Type[line[0]]=line[1]
            self.neuron2label_dict=Neuron2Type
            Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
            self.neu2ID_dict=Neuron2ID
            type_set=set(Neuron2Type.values())
            Type2id={k:v for v,k in enumerate(type_set)}
            self.label2ID_dict=Type2id
        return self.label2ID_dict
    @property
    def num_nodes(self):
        return self._data.num_nodes
    @property
    def typedim(self):
        if hasattr(self,'cache_type_dim'):
            return self.cache_type_dim
        else:
            label2ID=self.label2ID
            self.cache_type_dim=len(label2ID.keys())
            return self.cache_type_dim
    @property
    def neuron2label(self):
        if hasattr(self,'neuron2label_dict'):
            return self.neu2ID_dict
        else:
            Neuron2Type={}
            with open(osp.join(self.raw_dir,'%s-cell-type.txt'%(self.data_prefix)),'r') as fin:
                for i in fin.readlines():
                    line=i.strip().split('\t')
                    if len(line)==2:
                        Neuron2Type[line[0]]=line[1]
            self.neuron2label_dict=Neuron2Type
            Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
            self.neu2ID_dict=Neuron2ID
            type_set=set(Neuron2Type.values())
            Type2id={k:v for v,k in enumerate(type_set)}
            self.label2ID_dict=Type2id
        return self.neuron2label_dict
    
    @staticmethod
    def read_data(raw_dir,data_prefix):
        Neuron2Type={}
        with open(osp.join(raw_dir,'%s-cell-type.txt'%(data_prefix)),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split('\t')
                if len(line)==2:
                    Neuron2Type[line[0]]=line[1]
        Neuron2ID={k:v for v,k in enumerate(Neuron2Type.keys())}
        type_set=set(Neuron2Type.values())
        Type2id={k:v for v,k in enumerate(type_set)}

        edge_index_list=[]
        edge_weight=[]
        edge_attr=[]
        with open(osp.join(raw_dir,'%s-edge_list.txt'%(data_prefix)),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split('\t')
                if len(line)==4:
                    pre,post=Neuron2ID[line[0]],Neuron2ID[line[1]]
                    edge_index_list.append([pre,post])
                    edge_weight.append(float(line[2]))
                    edge_attr.append(1 if line[3]=='chem' else 0)
        

        edge_index=torch.tensor(edge_index_list)
        edge_weight=torch.tensor(edge_weight)
        edge_weight=edge_weight.to(torch.float32)
        edge_attr=torch.tensor(edge_attr)
        y=[Type2id[v] for _,v in Neuron2Type.items()]
        
        y=torch.tensor(y)

        x=torch.nn.functional.one_hot(y)
        x=x.to(dtype=torch.float32)
        edge_index=edge_index.T

        return Data(x=x,edge_index=edge_index,y=y,edge_attr=edge_attr,edge_weight=edge_weight)

    def process(self):
        data = self.read_data(self.raw_dir,self.data_prefix)
        data = data if self.pre_transform is None else self.pre_transform(data)
        torch.save(self.collate([data]), self.processed_paths[0])
    def manual_split(self,path):
        label2ID={}
        with open(osp.join(path,'label2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    label2ID[line[0]]=int(line[1])
        neu2ID={}
        with open(osp.join(path,'neu2ID.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    neu2ID[line[0]]=int(line[1])
        
        for k,v in self.neu2ID.items():
            if neu2ID[k]!=v:
                raise ValueError('this file doesn`t match this object(%s)'%__name__)

        test_edge_index=[]
        with open(osp.join(path,'test_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    test_edge_index.append([n1,n2])
        test_edge_index=torch.tensor(test_edge_index).T
        test_edge_index=test_edge_index.to(device=self.data.x.device)
        test_edge_label_index=torch.ones(test_edge_index.size(1),device=self.data.x.device)

        train_edge_index=[]
        with open(osp.join(path,'train_edge_list.txt'),'r') as fin:
            for i in fin.readlines():
                line=i.strip().split(' ')
                if len(line)==2:
                    n1,n2=int(line[0]),int(line[1])
                    train_edge_index.append([n1,n2])
        train_edge_index=torch.tensor(train_edge_index).T
        train_edge_index=train_edge_index.to(device=self.data.x.device)
        train_edge_label_index=torch.ones(train_edge_index.size(1),device=self.data.x.device)

        test_data=Data(x=self.data.x,y=self.data.y,edge_index=test_edge_index,edge_label_index=test_edge_label_index,neu2ID=neu2ID,label2ID=label2ID)
        train_data=Data(x=self.data.x,y=self.data.y,edge_index=train_edge_index,edge_label_index=train_edge_label_index,neu2ID=neu2ID,label2ID=label2ID)
        return train_data,test_data

    def __repr__(self) -> str:
        return 'Celegans19-%s'%self.name
class Celegans19_herm(Celegans19):
    def __init__(self,*args,**kwargs):
        kwargs['mode']='herm'
        super(self,Celegans19_herm).__init__(*args,**kwargs)
class DIYbrain_networks(InMemoryDataset):
    def __init__(self, root: str,split='node', transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None,process=False,restore_split=None,device=None):

        super().__init__(root, transform, pre_transform)
        if device is None:
            self.device='cpu'
        else:
            self.device=device
        if process:
            self._process()
        if restore_split is None:
            self.data, self.slices = torch.load(self.processed_paths[0],map_location=self.device)
        elif isinstance(restore_split,str):
            self.data= torch.load(restore_split,map_location=self.device)
        self.data, self.slices = self.collate([self.data])
class NxGraph(InMemoryDataset):
    url=None
    def __init__(self, root: Optional[str] = None, nxg='barbell',transform: Optional[Callable] = None, pre_transform: Optional[Callable] = None, pre_filter: Optional[Callable] = None,**kwargs):
        
        
        self.kwargs=kwargs
        if isinstance(nxg,str):

            self.name=nxg
            self.nxg=self.create_graph(self.name,**self.kwargs)

        elif isinstance(nxg,nx.Graph):
            self.nxg=nxg
            self.name=str(nxg)
        super().__init__(root, transform, pre_transform)
        self.data=torch_geometric.utils.from_networkx(self.nxg)
        self.data = self.data if self.pre_transform is None else self.pre_transform(self.data)
        self.data, self.slices = self.collate([self.data])
    @staticmethod
    def create_graph(opt,*args,**kwargs):

        if opt=='barbell':

            if ('m1' in kwargs) and ('m2' in kwargs):
                m1,m2=kwargs.pop('m1'),kwargs.pop('m2')
                nxg=nx.barbell_graph(m1,m2,**kwargs)
            raise ValueError('Barbell graph options error:%s'%str(kwargs))
        
        return nxg
    