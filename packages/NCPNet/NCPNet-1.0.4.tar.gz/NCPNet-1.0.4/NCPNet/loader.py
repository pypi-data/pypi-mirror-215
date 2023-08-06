import numpy as np
import torch
from torch_geometric.data import InMemoryDataset
from torch_geometric.utils import negative_sampling
import networkx as nx
import random


class LinkPred_Loader:
    def __init__(self,config,dataset: InMemoryDataset):
        self.dataset=dataset
        self.loader_config=config
        if 'negtive_num' in self.loader_config:
            self.negtive_num=self.loader_config['negtive_num']
        else:
            self.negtive_num=1

        if 'batch_size' in self.loader_config:
            self.batch_size=self.loader_config['batch_size']
        else:
            if dataset.edge_index.size(1)*(self.negtive_num+1)*self.loader_config['dim']<int(8*1024*1024*1024/12):
                self.batch_size=dataset.edge_index.size(1)
            else:
                self.batch_size=min(500000,dataset.edge_index.size(1))
        self.step=0
    def __iter__(self):
        self.step=0

        neg_edge_index = negative_sampling(
            edge_index=self.dataset.edge_index, num_nodes=self.dataset.num_nodes,
            num_neg_samples=self.dataset.edge_index.size(1)*self.negtive_num, method='sparse')
        self.edge_label_index = torch.cat(
            [self.dataset.edge_index, neg_edge_index],
            dim=-1
        )
        
        self.edge_label = torch.cat([
            self.dataset.edge_index.new_ones(self.dataset.edge_index.size(1),dtype=torch.float32),neg_edge_index.new_zeros(neg_edge_index.size(1),dtype=torch.float32)
        ], dim=0)
        perm = torch.randperm(self.edge_label_index.size(1),device=self.edge_label.device)
        self.batch_index=torch.split(perm,self.batch_size)
        # split_num=ceil(self.edge_label_index.size(1)/self.batch_size)
        # self.batchs_edge_index=torch.hsplit(self.edge_label_index,split_num)
        self.edge_label_index=self.edge_label_index.T
        self.edge_label=self.edge_label.T
        return self
    def __next__(self):
        if self.step>=len(self.batch_index):
            raise StopIteration
        else:
            ind=self.batch_index[self.step]
            edge_label_index=torch.nn.functional.embedding(ind,self.edge_label_index)
            edge_label_index=edge_label_index.T
            edge_label=torch.nn.functional.embedding(ind,self.edge_label)
            edge_label=edge_label.T
            batch=(self.dataset.x,self.dataset.edge_index,self.dataset.edge_attr,edge_label_index,edge_label)
            self.step+=1
        return batch
    def __len__(self):
        return len(self.batch_index)
class LinkPred_PairNeigh_Loader(LinkPred_Loader):
    def __init__(self,config,dataset: InMemoryDataset,nxg:nx.Graph,hop=1):
        self.dataset=dataset
        self.loader_config=config
        if 'negtive_num' in self.loader_config:
            self.negtive_num=self.loader_config['negtive_num']
        else:
            self.negtive_num=1

        if 'batch_size' in self.loader_config:
            self.batch_size=self.loader_config['batch_size']
        else:
            if dataset.edge_index.size(1)*(self.negtive_num+1)*self.loader_config['dim']<int(8*1024*1024*1024/12):
                self.batch_size=dataset.edge_index.size(1)
            else:
                self.batch_size=min(500000,dataset.edge_index.size(1))
        self.nxg={}
        for n in nxg.nodes():
            self.nxg[n]=set(nxg[n])
        for i in range(dataset.num_nodes):
            if i not in self.nxg:
                self.nxg[i]=set([])
        for i in range(hop-1):
            for n in self.nxg.keys():
                q=list(self.nxg[n])
                for j in q:
                    if j !=n:
                        for kj in self.nxg[j]:
                            if kj not in self.nxg[n] and kj!=n:
                                self.nxg[n].add(kj)
        self.cached_nxg_neighbors=None
        self.step=0
        self.max_pad_num=None
    
    def get_neighboor(self,edge_index,mode='inter',max_num=30):
        edge_index_list=edge_index.cpu().T.tolist()
        res=[]
        
     
        if mode=='inter':
  
            for edges in edge_index_list:
                u,v=tuple(edges)
                u_set,v_set=self.nxg[u],self.nxg[v]

                pair=u_set.intersection(v_set)
                pair=pair.difference({u,v})
                neigh=list(pair)
                if len(neigh)>max_num:
                    #random.sample(neigh,max_num)
                    res.append(random.sample(neigh,max_num))
                else:
                    res.append(neigh)
        res=[torch.tensor(i,dtype=torch.int32)+1 for i in res]
        out=torch.nn.utils.rnn.pad_sequence(res,batch_first=False).T
        return out
    def __iter__(self):
        self.step=0
        neg_edge_index = negative_sampling(
            edge_index=self.dataset.edge_index, num_nodes=self.dataset.num_nodes,
            num_neg_samples=self.dataset.edge_index.size(1)*self.negtive_num, method='sparse')
        if self.cached_nxg_neighbors is None:
            self.cached_nxg_neighbors=self.get_neighboor(self.dataset.edge_index)

        neg_nxg_neighbors=self.get_neighboor(neg_edge_index)

        if neg_nxg_neighbors.size(1)<self.cached_nxg_neighbors.size(1):
            d=self.cached_nxg_neighbors.size(1)-neg_nxg_neighbors.size(1)
            neg_nxg_neighbors=torch.cat([neg_nxg_neighbors,torch.zeros(size=(neg_nxg_neighbors.size(0),d),dtype=torch.int32)],dim=1)
        elif neg_nxg_neighbors.size(1)>self.cached_nxg_neighbors.size(1):
            d=neg_nxg_neighbors.size(1)-self.cached_nxg_neighbors.size(1)
            self.cached_nxg_neighbors=torch.cat([self.cached_nxg_neighbors,torch.zeros(size=(self.cached_nxg_neighbors.size(0),d),dtype=torch.int32)],dim=1)
        assert self.cached_nxg_neighbors.size(1)==neg_nxg_neighbors.size(1)

        self.neighbors=torch.cat([self.cached_nxg_neighbors,neg_nxg_neighbors],dim=0)
        self.neighbors=self.neighbors.to(device=self.loader_config['device'])
        self.edge_label_index = torch.cat(
            [self.dataset.edge_index, neg_edge_index],
            dim=-1
        )
        
        self.edge_label = torch.cat([
            self.dataset.edge_index.new_ones(self.dataset.edge_index.size(1),dtype=torch.float32),neg_edge_index.new_zeros(neg_edge_index.size(1),dtype=torch.float32)
        ], dim=0)
        perm = torch.randperm(self.edge_label_index.size(1),device=self.edge_label.device)
        self.batch_index=torch.split(perm,self.batch_size)
        # split_num=ceil(self.edge_label_index.size(1)/self.batch_size)
        # self.batchs_edge_index=torch.hsplit(self.edge_label_index,split_num)
        self.edge_label_index=self.edge_label_index.T
        return self
    def __next__(self):
        if self.step>=len(self.batch_index):
            raise StopIteration
        else:
            ind=self.batch_index[self.step]
    
            edge_label_index=self.edge_label_index[ind]
            edge_label_index=edge_label_index.mT
   
            edge_label=self.edge_label[ind]
            #edge_label=self.edge_label[ind]
            #edge_label=edge_label.mT
            batch_neighbor=self.neighbors[ind]
            batch=(self.dataset.x,self.dataset.edge_index,self.dataset.edge_attr,edge_label_index,edge_label,batch_neighbor)
            self.step+=1
        return batch
    def __len__(self):
        return len(self.batch_index)

class NodeCla_Loader:
    '''for small graph'''
    def __init__(self,dataset: InMemoryDataset):
        self.dataset=dataset
        self.batch_num=1
        self.step=0
    def __iter__(self):
        self.step=0
        return self
    def __next__(self):
        if self.step >= self.batch_num:
            raise StopIteration
        batch=(self.dataset.x, self.dataset.edge_index,self.dataset.edge_attr,self.dataset.y,self.dataset.train_mask,self.dataset.test_mask)
        self.step+=1
        return batch
class Scale_NodeCla_Loader:
    def __init__(self,dataset: InMemoryDataset,subgraph_num=40,shuffle=True):
        self.dataset=dataset
        self.batch_num=subgraph_num
        self.step=0
        self.subgraph_num=subgraph_num
        self.chunk_size=int(self.dataset.edge_index.size()[1]/self.subgraph_num)
        self.shuffle=shuffle
        #self.update()
    def update(self):
        edge_index=self.dataset.edge_index
        edge_idx=np.arange(0,edge_index.size()[1])
        if self.shuffle:
            np.random.shuffle(edge_idx)
        device=edge_index.data.device
        self.iter_idx=torch.split(torch.from_numpy(edge_idx).to(device=device),self.chunk_size)
    def __iter__(self):
        self.update()
        return self
    def __next__(self):
        if self.step >= self.batch_num:
            raise StopIteration
        else:
            batch_id=self.iter_idx[self.step]
            batch_edge_index=torch.nn.functional.embedding(batch_id,self.dataset.edge_index.T)
            batch_edge_index=batch_edge_index.T
            batch=(self.dataset.x, batch_edge_index,self.dataset.edge_attr,self.dataset.y,self.dataset.train_mask,self.dataset.test_mask)
            self.step+=1
        return batch