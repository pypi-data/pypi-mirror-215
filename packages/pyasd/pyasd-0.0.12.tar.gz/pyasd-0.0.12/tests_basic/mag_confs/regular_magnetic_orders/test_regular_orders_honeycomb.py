#!/usr/bin/env python

import numpy as np
import glob
import pickle
from asd.utility.spin_visualize_tools import *
from asd.core.geometry import *
from asd.core.spin_configurations import regular_order, init_random
import itertools

lat_type='honeycomb'
nx=4
ny=4
latt,sites = build_latt(lat_type,nx,ny,1,return_neigh=False)
sites_cart = np.dot(sites,latt)
nat=sites.shape[-2]

conf_names = ['Stripy','super-Neel','Neel','Zigzag','FM']
for conf_name in conf_names:

    sp_lat_uc = regular_order(lat_type,conf_name)
    sp_lat = np.zeros((nx,ny,nat,3))
    rx=range(0,nx,2)
    ry=range(0,ny,2)
    for i,j in itertools.product(rx,ry):
        sp_lat[i:i+2,j:j+2] = sp_lat_uc

    spins = np.swapaxes(sp_lat,0,1).reshape(-1,3)
    params = gen_params_for_ovf(nx,ny,2)
    write_ovf(params,spins,'conf_{}.ovf'.format(conf_name))
    plot_spin_2d(sites_cart,sp_lat,show=True,scatter_size=100,
    superlatt=np.dot(np.diag([nx,ny]),latt),colorbar_shrink=0.3,title=conf_name)
    #pickle.dump(sp_lat,open('conf_{}.pickle'.format(conf_name),'wb'))

sp_lat = np.zeros((nx,ny,2,3))
sp_lat = init_random(sp_lat)
spins = np.swapaxes(sp_lat,0,1).reshape(-1,3)
params = gen_params_for_ovf(nx,ny,2)
nn = len(glob.glob('conf_random*ovf'))
fil = 'conf_random_{}.ovf'.format(nn+1)
write_ovf(params,spins,fil)
plot_spin_2d(np.dot(sites,latt),sp_lat,show=True,scatter_size=20,colorbar_shrink=0.3,title='random')
 
