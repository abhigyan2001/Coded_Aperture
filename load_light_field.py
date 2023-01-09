# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 21:12:46 2023
@author: Hp
"""

import os
import numpy as np 
import cv2
import matplotlib.pyplot as plt

def split_stack(img_stack, crop_factor):
    img_width = 1024
    img_height = 1024
    stack_shape = img_stack.shape
    stack_depth = stack_shape[2] // 3

    cropped_size = 1024 // crop_factor
    ## NCHW
    stack_id = 0
    overall_stack = np.zeros([crop_factor * crop_factor * 3, stack_depth, cropped_size, cropped_size])
    for c in range(3):
        for i in range(crop_factor):
            for j in range(crop_factor):             
                stack_slice = img_stack[i*cropped_size:i*cropped_size+cropped_size,j*cropped_size:j*cropped_size+cropped_size,c*stack_depth:(c+1)*stack_depth]
                for channel in range(stack_depth):
                    print(stack_id, i , j, c)
                    overall_stack[stack_id, channel, :, :] = stack_slice[:,:,channel]
                    
                stack_id+= 1

    return overall_stack



def process_lf(file_path_list, crop_factor):
    img_width = 1024
    img_height = 1024 
    img_stack_size = len(file_path_list)    
    img_stack = np.zeros([img_height, img_width, img_stack_size*3])
    i = 0 


    for file_path in file_path_list:
        
        img = cv2.imread(file_path)
        img = np.asarray(img, dtype= 'float')

        r = img[:, :, 0]
        g = img[:, :, 1]
        b = img[:, : , 2]

        img_stack[:,:, i] = r
        img_stack[:, :, img_stack_size + i] = g 
        img_stack[:, :, img_stack_size * 2 + i] = b 

        i += 1
        
    img_stack = split_stack(img_stack, crop_factor)
    print(img_stack.shape)
    return img_stack

def load_lf():
    ## Declaring Constants 
    img_width = 1024
    img_height = 1024

    crop_factor = 8


    scene_names = ['BarcaArchVis' , 'Classroom'] #, 'Cupcakes', 'RippleDreams', 'Splash33']


    overall_lf = np.empty(shape= [0, 25, 128, 128])
    for scene_name in scene_names:

        directory = "C:/Users/Hp/Documents/Coded_aperture/Dataset_full"
        range_of_depths = [1, 9, 0.05]

        plane_depth = float(range_of_depths[0])
        max_depth = range_of_depths[1]
        increment = range_of_depths[2]

        directory = os.path.join(directory, scene_name)
        directory = os.path.join(directory, 'Multifocal/Lightfield')

        file_path_list = []
        for file in os.listdir(directory):
            if '0' not in  file:

                continue
            file_path_list.append(os.path.join(directory, file))

        lf_stack = process_lf(file_path_list, crop_factor)
        overall_lf = np.append(overall_lf, lf_stack, axis = 0)


        return overall_lf




         