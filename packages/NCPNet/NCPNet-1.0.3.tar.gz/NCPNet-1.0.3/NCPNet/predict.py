

import random
from time import time
import numpy as np
import torch
import os
import torch_geometric
import sys
import os.path as osp

import traceback
import copy
import argparse
import yaml
from NCPNet.brain_data import HemiBrain,LinkPred_Loader,Celegans19,LinkPred_PairNeigh_Loader

import torch_geometric.transforms as T
from NCPNet.approaches import Net
from NCPNet.utils import load_config,edge_index2Graph
from NCPNet.task import Base_Task
from torch_geometric.loader import RandomNodeSampler,NeighborLoader
from torch_geometric.transforms import RandomLinkSplit
from NCPNet.trainer import LinkPred_trainer
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',type=str, default='model.ncpnet')
    parser.add_argument('-pred',type=str,nargs=2,default=['0','0'])
    parser.add_argument('-d',default='cpu')
    parser.add_argument('-datadir',type=str,default=None)
    args = parser.parse_args()
    return args
class Inferrer:
    def __init__(self,modelfile,device='cpu'):
        if not torch.cuda.is_available() and 'cuda' not in device:
            device='cpu'
        print('Initilizing an Inferrer from %s'%modelfile)
        self.model=torch.load(modelfile)
        self.model.to(device=device)
        self.neu2embid=self.model.train_data.neu2ID
    @staticmethod
    def infer():
        args=parse_args()
        self=Inferrer(args.m,device=args.d)
        uuid_u,uuid_v=tuple(args.pred)
        print('Inferring the connection probability of (%s->%s)'%(uuid_u,uuid_v))
        score=self._infer(uuid_u,uuid_v)
        print('The score of (%s->%s): %.3f'%(uuid_u,uuid_v,score))
        
    def _infer(self,uuid_u,uuid_v):
        if uuid_u not in self.neu2embid:
            raise KeyError('ID%s is not in the model..please check'%uuid_u)
        if uuid_v not in self.neu2embid:
            raise KeyError('ID%s is not in the model..please check'%uuid_v)
        u,v=self.neu2embid[uuid_u],self.neu2embid[uuid_v]
        score=self.model.infer_connection(u,v).detach().cpu()
        return score
        
        
    
    
    


