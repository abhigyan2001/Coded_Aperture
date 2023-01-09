# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 21:12:46 2023
@author: Hp
"""

import os
import numpy as np 
import cv2
import matplotlib.pyplot as plt

def split_stack(img_stack, crop_factor = 8):
    
    stack_shape = img_stack.shape
    stack_depth = stack_shape[2]//3

    cropped_size = 1024 // crop_factor

    overall_stack = np.zeros([crop_factor * crop_factor * 3, stack_depth, cropped_size, cropped_size])
    tick = 0
    for c in range(3):
        for i in range(crop_factor):
            for j in range(crop_factor):
                stack_slice = img_stack[i*cropped_size:i*cropped_size+cropped_size,j*cropped_size:j*cropped_size+cropped_size,c*stack_depth:(c+1)* stack_depth]
                #print(stack_slice.shape, c, i , j)
                for channel in range(stack_depth):
                    overall_stack[tick, channel, :, :] = stack_slice[:, :, channel]

                tick +=1 

    return overall_stack



def process_scene(file_path_list):
    crop_factor = 8
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
    return img_stack

def load_targets():
#if __name__ == "__main__":
    ## Declaring Constants 
    img_width = 1024
    img_height = 1024

    crop_factor = 8


    scene_names = ['BarcaArchVis', 'Classroom']#, 'Cupcakes', 'RippleDreams', 'Splash33']

    overall_targets = np.empty(shape=[0, 41, 128, 128])

    for scene_name in scene_names:

        directory = "C:/Users/Hp/Documents/Coded_aperture/Dataset_full"
        range_of_depths = [1, 9, 0.05]

        plane_depth = float(range_of_depths[0])
        max_depth = range_of_depths[1]
        increment = range_of_depths[2]

        directory = os.path.join(directory, scene_name)
        directory = os.path.join(directory, 'Multifocal')

        file_path_list = []
        for file in os.listdir(directory):
            
            img_id = '{:.2f}.png'.format(plane_depth)

            if img_id in file:
                file_path_list.append(os.path.join(directory, file))
                plane_depth += 0.05
 
        img_stack = process_scene(file_path_list)
        overall_targets = np.append(overall_targets, img_stack, axis=0 )    
    return overall_targets




            
        



