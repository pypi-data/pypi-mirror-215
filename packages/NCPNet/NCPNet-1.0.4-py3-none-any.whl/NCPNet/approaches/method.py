
import torch
from .Encoder import GCN,GCN2,MLP,node_attr_encoder
from .Decoder import LinkPred
from .PairEncoder import NeighEnco,NeighEnco2
from os.path import join
import pickle
import yaml
import os
from NCPNet.utils import edge_index2Graph
from NCPNet.loader import LinkPred_PairNeigh_Loader
import random
class Net(torch.nn.Module):
    def __init__(self,config,cache_nxg=False):
        super(Net,self).__init__()
        self.config=config
        node_encoder=self.config['node_encoder']
        if 'pair_encoder' in self.config:
            pair_encoder=self.config['pair_encoder']
            self.use_pair_enco=True
            if'gamma' in self.config:
                self.gamma=self.config['gamma']
            else:
                self.gamma=0.5
        else:
            self.use_pair_enco=False
        decoder=self.config['Model']
        namespace=globals()
        if decoder in namespace and node_encoder in namespace:
            Deco_cls,node_Enco_cls=namespace[decoder],namespace[node_encoder]
            self.Deco,self.node_Enco=Deco_cls(config),node_Enco_cls(config)
        else:
            raise ModuleNotFoundError('%s or %s not found'%(decoder,node_encoder))
        if self.use_pair_enco:
            if pair_encoder in namespace:
                pair_encoder_cls=namespace[pair_encoder]
                self.pair_Enco=pair_encoder_cls(config)
                self.ga=torch.nn.parameter.Parameter(data=torch.tensor([self.gamma]),requires_grad=False)
            else:
                raise ModuleNotFoundError('%s not found'%(pair_encoder))
        self.train_data=None
        self.nxg=None
        #for predicting
        self.X=None
        self.z=None
        self.cache_nxg=cache_nxg
    def _store_train_edges(self,train_data=None):
        if (self.train_data is None) and (train_data is None):
            raise ValueError('Please provide train_data..')
        if self.train_data is None and (train_data is not None):
            self.train_data=train_data
        if not hasattr(self,'train_edges'):
            self.X=torch.nn.parameter.Parameter(data=self.train_data.data.x.detach(),requires_grad=False)
            with torch.no_grad():
                z=self.node_Enco(x=self.X,edge_index=self.train_data.data.edge_index)
                self.z=torch.nn.parameter.Parameter(data=z.detach(),requires_grad=False)
            
    def forward(self,*args,**kwargs):
        z=self.node_Enco(x=kwargs['x'],edge_index=kwargs['edge_index'])
        if self.use_pair_enco:

            out=self.Deco(z,edge_label_index=kwargs['edge_label_index'],neighbor=kwargs['neighbor'])
        else:
            out=self.Deco(z,edge_label_index=kwargs['edge_label_index'])
        return out
    def _create_setnxg(self,nxg):
        
        self.nxg={}
        for n in nxg.nodes():
            self.nxg[n]=set(nxg[n])
        for i in range(self.train_data.num_nodes):
            if i not in self.nxg:
                self.nxg[i]=set([])
        if self.cache_nxg:
            for i in range(self.config['hop']-1):
                for n in self.nxg.keys():
                    q=list(self.nxg[n])
                    for j in q:
                        if j !=n:
                            for kj in self.nxg[j]:
                                if kj not in self.nxg[n] and kj!=n:
                                    self.nxg[n].add(kj)
    def get_neighboor(self,u,v,mode='inter',max_num=30):
        if self.nxg==None and self.train_data is not None:
            nxg=edge_index2Graph(self.train_data.data.edge_index)
            nxg.to_undirected()
            self._create_setnxg(nxg)
        assert self.nxg!=None
        res=[]
        if mode=='inter':
            if self.cache_nxg:
                u_set,v_set=self.nxg[u],self.nxg[v]
            else:
                u_set,v_set=self.nxg[u],self.nxg[v]
                for i in range(self.config['hop']-1):
                    temp_u_set,temp_v_set=set([]),set([])
                    for i in u_set:
                        for n in self.nxg[i]:
                            temp_u_set.add(n)
                    for i in v_set:
                        for n in self.nxg[i]:
                            temp_v_set.add(n)
                    u_set,v_set=u_set.union(temp_u_set),v_set.union(temp_v_set)
                    
            pair=u_set.intersection(v_set)
            pair=pair.difference({u,v})    
            neigh=list(pair)
            if len(neigh)>max_num:
                res.append(random.sample(neigh,max_num))
            else:
                res.append(neigh)
        res=[torch.tensor(i,dtype=torch.int32)+1 for i in res]
        out=torch.nn.utils.rnn.pad_sequence(res,batch_first=False).T
        return out
    def infer_connection(self,u,v):
        pair=torch.tensor([[u],[v]])
        if self.use_pair_enco and self.train_data is not None:
            if self.nxg== None:
                nxg=edge_index2Graph(self.train_data.data.edge_index)
                nxg.to_undirected()
                self._create_setnxg(nxg)
            if self.use_pair_enco:
                neighbors=self.get_neighboor(u,v,max_num=4)
                neighbors=neighbors.contiguous()
                out=self.Deco(self.z,pair,neighbor=neighbors)
            else:
                out=self.Deco(self.z,pair)
        return out
    @torch.no_grad()
    def NodeCla_inference(self,x_all, subgraph_loader):
        xs = []
        for batch in subgraph_loader:
            batch.to(device=self.config['device'])
            x = x_all[batch.n_id.to(x_all.device)]
            x=self.node_Enco.node_attr_layer(x)
            x = self.node_Enco.conv1(x, batch.edge_index)
            x=self.node_Enco.relu1(x)
            xs.append(x[:batch.batch_size].cpu())
        x_all = torch.cat(xs, dim=0).to(device=self.config['device'])
        xs = []
        for batch in subgraph_loader:
            batch.to(device=self.config['device'])
            x = x_all[batch.n_id.to(x_all.device)]
            x = self.node_Enco.conv2(x, batch.edge_index)
            xs.append(x[:batch.batch_size].cpu())
        x_all = torch.cat(xs, dim=0).to(device=self.config['device'])
        return x_all
    def make(self,path:str,train_data,name='checkpoint'):
        self._store_train_edges(train_data)
        with open(join(path,name+'.m'), 'wb') as pkl:
            if self.use_pair_enco and self.train_data is not None:
                pickle.dump((self,train_data,self.config),pkl)
            else:
                pickle.dump((self,self.config),pkl)
    @staticmethod
    def loadfrom(filepath):
        with open(filepath,'rb') as fin:
            model,train_data,config=pickle.load(fin)
        if model.train_data is None:
            model.train_data=train_data
        return model
