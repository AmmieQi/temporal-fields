"""
Asynchronous Temporal Fields Base model
"""
import torch.nn as nn
import torch
from torch.autograd import Variable


class AsyncTFBase(nn.Module):
    def __init__(self, dim, nclasses, nhidden):
        super(AsyncTFBase, self).__init__()
        self.nc = nclasses
        self.mA = nn.Linear(dim, nclasses)
        # self.mAA = nn.Linear(1, nclasses * nclasses)
        self.naa = nhidden
        # self.mAAa = nn.Sequential(nn.Linear(1, self.nc * self.naa, bias=False),
        #                           nn.Dropout())
        # self.mAAb = nn.Sequential(nn.Linear(1, self.naa * self.nc, bias=False),
        #                           nn.Dropout())
        self.mAAa = nn.Linear(1, self.nc * self.naa, bias=False)
        self.mAAb = nn.Linear(1, self.naa * self.nc, bias=False)

    def forward(self, x):
        a = self.mA(x)
        const = Variable(torch.ones(a.shape[0], 1).cuda())
        # aa = self.mAA(const)
        aaa = self.mAAa(const).view(-1, self.nc, self.naa)
        aab = self.mAAb(const).view(-1, self.naa, self.nc)
        aa = torch.bmm(aaa, aab)

        # aa = torch.zeros(*aa.shape)
        # for i in range(a.shape[0]):
        #     aa[i, :] = torch.eye(a.shape[1])[:]
        # aa = Variable(aa.cuda())

        return a, aa.view(-1, self.nc, self.nc)
