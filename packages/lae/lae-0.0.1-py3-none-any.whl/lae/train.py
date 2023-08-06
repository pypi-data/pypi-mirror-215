#!/usr/bin/env python
# coding: utf-8

#Linearization autoencoder, GPL
'''
Train a linearization autoencoder model on a custom dataset

Usage:
    import train;
    train.run(data='data/ex', tolerance=3, plot_loss=True, vis_latent=True, vis_prediction=True)
or
    python train.py --data data/ex --tolerance 3 --plot_loss True --vis_latent True --vis_prediction True
'''

import argparse
import sys
import os
from pathlib import Path
import torch
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd
import torch.nn as nn
import itertools
from torch.utils.data.dataloader import default_collate


import utils.read_data as rd
from utils.analysis import test_model
import utils.signal_merger as merger

class Dataset():
    def __init__(self, data, phase):
        merger.signal_merger(data)
        self.X, self.y = rd.getData(os.path.join(Path(data).parents[0],str(Path(data).name)+'_merge_data.csv'), phase)
    def __len__(self):
        return len(self.X)
    def __getitem__(self, idx):
        X = self.X[idx]
        y = self.y[idx]
        sig_tensor = torch.from_numpy(np.array(X)).to(torch.float32)

        return sig_tensor, y

# Build a model
class LAE(torch.nn.Module):
    def __init__(self, input_dimension, layerinfo):
        super().__init__()
        layers = [input_dimension] + layerinfo
        enc_size = layers
        dec_size = enc_size[::-1]
        enc_blocks = [torch.nn.Linear(in_f, out_f) for in_f, out_f in zip(enc_size, enc_size[1:])]
        self.encoder = torch.nn.Sequential(*enc_blocks)
        dec_blocks = [torch.nn.Linear(in_f, out_f) for in_f, out_f in zip(dec_size, dec_size[1:])]
        self.decoder = torch.nn.Sequential(*dec_blocks)

    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

# Loss function
def calculate_loss(y, latent, tol):
    pdist = nn.PairwiseDistance(p=2)
    tolerance = tol
    totalL2 = torch.tensor(0)
    l2count = 1
    pairs = list(itertools.combinations(list(range(0, len(y))), 2))
    for i in range(len(pairs)):
        a = pairs[i][0]
        b = pairs[i][1]
        difference = abs(y[a] - y[b])
        if difference < tolerance:
            totalL2 = totalL2 + pdist(latent[a], latent[b])
            l2count = l2count + 1
    totalL2 = totalL2 / l2count
    totalL3 = 0
    for i in range(len(y)):
        this_conc_pos = [y[i], y[i]]
        l3 = pdist(latent[i][0], torch.tensor(this_conc_pos)[0])
        totalL3 = totalL3 + l3
    totalL3 = totalL3 / len(y)
    return totalL2, totalL3

# Training
def train(opt):
    print('current device: ', torch.cuda.current_device(), ' ', torch.cuda.get_device_name(torch.cuda.current_device()))
    device = torch.cuda.current_device()
    datasets = Dataset(opt.data, 'train')
    loader = DataLoader(dataset=datasets, batch_size=opt.batch_size, shuffle=True, collate_fn=lambda x: tuple(x_.to(device) for x_ in default_collate(x)))
    input_dimension = len(list(loader.dataset[0][0]))
    layer_info = opt.layers
    layer_info = layer_info + [2]
    model= LAE(input_dimension, layer_info)
    model.to(device)

    loss_function = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr, weight_decay=opt.wd)

    epochs = opt.epoch
    losses = []
    loss1s = []
    loss2s = []
    loss3s = []
    for epoch in range(epochs):
        if epoch % 10 == 0:
            print('epoch: ', epoch)
        for (signal, y) in loader:
            reconstructed = model(signal)
            latent = model.encoder(signal)
            loss1 = loss_function(reconstructed, signal)
            loss2, loss3 = calculate_loss(y, latent, tol=opt.tolerance)
            loss1 = loss1 * opt.loss_coef[0]
            loss2 = loss2 * opt.loss_coef[1]
            loss3 = loss3 * opt.loss_coef[2]
            loss = loss1 + loss2 + loss3

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            losses.append(loss.cpu().detach().numpy())
            loss1s.append(loss1.cpu().detach().numpy())
            loss2s.append(loss2.cpu().detach().numpy())
            loss3s.append(loss3.cpu().detach().numpy())

    torch.save(model, 'result/' + opt.name + '.pth')

    # Defining the Plot Style
    if opt.plot_loss == True:
        plt.style.use('seaborn-white')
        plt.xlabel('Iterations')
        plt.ylabel('Loss')

        plt.plot(losses[1:], c='darkgrey', linewidth=4, alpha=1)
        plt.plot(loss1s[1:], c='tab:green', linewidth=0.5)
        plt.plot(loss3s[1:], c='tab:red', linewidth=0.5)
        plt.plot(loss2s[1:], c='tab:brown', linewidth=.5)
        plt.show()
        plt.clf()
        r2 = test_model(opt.name+'.pth', opt)

def main(opt):
    torch.cuda.set_device(opt.device)
    train(opt)

# Parse arguments
def parse_opt(known=False):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='./data/ex') # data location
    parser.add_argument('--batch_size', type=int, default = 32) # batch size
    parser.add_argument('--device', default='cuda:0') # device
    parser.add_argument('--lr', default=1e-4) # learning rate
    parser.add_argument('--wd', default=1e-5) # weight decay
    parser.add_argument('--epoch', default= 200) # epoch
    parser.add_argument('--tolerance', type=int,  default= 0) # tolerance
    parser.add_argument('--layers', default= [10,10]) # hidden layer structure (input - hidden layer - 2 (latent))
    parser.add_argument('--loss_coef', default= [1,1,10]) # coefficients for each losses
    parser.add_argument('--name', default='test') # name of saved model ('name'.pth)
    parser.add_argument('--plot_loss', default=False, type=lambda x: (str(x).lower in ['true', 'yes', '1']))
    parser.add_argument('--vis_latent', default=False, type=lambda x: (str(x).lower in ['true', 'yes', '1']))
    parser.add_argument('--vis_prediction', default=False, type=lambda x: (str(x).lower in ['true', 'yes', '1']))

    opt = parser.parse_known_args()[0] if known else parser.parse_args()
    return opt

def run(**kwargs):
    opt = parse_opt(True)
    for i, j in kwargs.items():
        setattr(opt, i, j)
    main(opt)

if __name__ == '__main__':
    opt = parse_opt(True)
    main(opt)

#run(data='data/ftir.csv', tolerance=3, plot_loss=True, vis_latent=True, vis_prediction=True)
torch.cuda.empty_cache()


