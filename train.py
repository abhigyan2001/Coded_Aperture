import os 
import numpy as np 
import matplotlib.pyplot as plt
import load_targets
import load_light_field
import torch 
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils




# Defining the Dataset 

class LFDataset(Dataset):
    """light Field Dataset."""

    def __init__(self, transform=None):
        """

        """
        self.training_data = load_light_field.load_lf()
        print('training_data loaded')
        self.targets =load_targets.load_targets()
        print('targets loaded')
        self.transform = transform

    def __len__(self):
        return len(self.training_data)

    def __getitem__(self, idx):

        sample = self.training_data[idx, :, :, :]
        target = self.targets[idx, :, :, :]

        if self.transform:4
data_set = LFDataset()
for i in range(0, len(data_set)), 40:
    sample = data_set[i]
    print(sample.shape)





