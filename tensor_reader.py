import numpy as np
import cv2
import torch
import os

datasets = ['BarcaArchVis','Classroom','Cupcakes','RippleDreams','Splash']
dnames = ['vis_','Classroom_','Cupcakes_','bubbly_','Splash33_']
for dataset,dname in zip(datasets,dnames):
    files = os.listdir(dataset)
    for f in files:
        if dname == f[:len(dname)]:
            file = os.path.join(dataset,f)
            img = cv2.imread(file)
