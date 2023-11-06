# -*- coding: utf-8 -*-
"""
@author: Kyriakos Fotiou
"""

import SimpleITK as sitk
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from scipy.spatial import distance
import statistics
import itertools
from collections import Counter
from scipy import ndimage




"""
Visualisation
"""
plt.style.use("seaborn-poster")
### Load Patient's CT Scan for Visualisation purposes ###
ct = np.load('ct_ave.npy')


### Mask Tumour Arrays ###
itv_masked =  np.ma.masked_where(itv == 0, itv)
ictv_masked =  np.ma.masked_where(ictv == 0, ictv)
ptv_masked =  np.ma.masked_where(ptv == 0, ptv)
### Plot Radiotherapy Volumes ###
plt.figure('GTV,CTV,PTV')
plt.imshow(ct[35,:,:], cmap = 'gray')
plt.imshow(ictv_masked[34,:,:],alpha = 0.7, vmin = 0)
plt.imshow(ptv_masked[33,:,:], alpha = 0.7 ,cmap= 'Blues', vmin = 0)
plt.imshow(itv_masked[35,:,:],alpha = 0.7,cmap = 'Reds', vmin = 0)
plt.xticks([])
plt.yticks([])
plt.show()


### Tumour Volume ### 
plt.figure (figsize=(5,3))
plt.title('Volume Variation')
phases = np.arange(0, 91, 10) # generate an array with phase values
plt.bar(phases, tumor_volumes, width = 8, align = 'center', linewidth=4)
plt.xlabel('Phase')
plt.ylabel('Tumor Volume [cc]')
plt.xticks(np.linspace(0,90,10)) 
plt.grid(axis = 'y')
plt.show()



### Centre of Mass ###
fig = plt.figure('Centre of Mass')
ax = fig.add_subplot(111, projection='3d')
plt.title('Centre of Mass')
for i, com in enumerate(com_list):
    ax.scatter(*com, cmap='tab10', alpha=1, label=str(i))   
x, y, z = zip(*com_list)
ax.plot(x, y, z, ':k')
ax.legend(loc = 'best')
ax.set_xlabel("SI", labelpad =25)
ax.set_ylabel("AP" ,labelpad =25 )
ax.set_zlabel("RL", labelpad =25)
plt.locator_params(axis='both', nbins=5)
plt.show()


### Probability Map ###
fig2= plt.figure('Probability Map')
ax = plt.subplot(111, projection ='3d') 
z,y,x = np.nonzero(prob_map)
pm =ax.scatter(z,y,x  ,c=prob_map[z,y,x ] ,cmap='tab10')
ax.set_xlabel('SI')
ax.set_ylabel('AP')
ax.set_zlabel('RL')
num1 = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '1']
handles = [plt.plot([],[],color=pm.cmap(pm.norm(float(num))), ls="", marker="s")[0] for num in num1]
# Add legend
ax.legend(handles, num1, loc='center right',fontsize='medium')
ax.set_xlabel('SI', labelpad=20)  
ax.set_ylabel('AP', labelpad=20)
ax.set_zlabel('RL', labelpad=20)
# Change tick interval for each axis
ax.xaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=5))
ax.yaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins= 5))
ax.zaxis.set_major_locator(MaxNLocator(integer=True, prune='both', nbins=5))
plt.show()




