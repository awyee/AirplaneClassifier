#Created Nov 3, 2018 by Alexander Yee

import numpy as np
import sys
import random
import os
from six.moves import cPickle as pck
import time
from PIL import Image

Inputfolderpath='../../Pics/Processed_downsampled/'
Outputfolderpath='../../Pickles/'
pixels_lengthwise=400
pixels_depthwise=400
RGB_channels=3
frac_val=0.2
frac_test=0.1
PIXEL_MAX_VALUE=255
pickle_batch_size=500

no_processed_images=0

test_size=50

def make_dataset_arrays(num_pics, num_labels):
    data = np.ndarray((num_pics, pixels_lengthwise, pixels_depthwise, RGB_channels), dtype=np.float16)
    labels = np.ndarray((num_pics, num_labels), dtype=np.int8)
    return data, labels

def read_pic_from_file(file_path):
    img = Image.open(file_path)
    #img = img.resize((IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)  # downsample image
    pixel_values = np.array(img.getdata()).reshape(img.size[1], img.size[0], 3)
    global no_processed_images
    no_processed_images+=1
    if no_processed_images%100==0:
        curtime=time.time()
        print('Processed %i images in %f seconds' %(no_processed_images, curtime-starttime))
    return pixel_values

def normalize_data(data):
    return (data - PIXEL_MAX_VALUE/ 2.0) / PIXEL_MAX_VALUE

def shuffle_data(data, labels):
    permutation = np.random.permutation(labels.shape[0])
    shuffled_dataset = data[permutation, :, :, :]
    shuffled_labels = labels[permutation, :]
    return shuffled_dataset, shuffled_labels

def read100images(planename):
    picfolder=pic_file = os.path.join(Inputfolderpath, planename)
    pics = os.listdir(picfolder)
    data = np.ndarray((test_size, pixels_lengthwise, pixels_depthwise, RGB_channels), dtype=np.float16)
    for i in range(0,test_size):
        new_pic_file = os.path.join(Inputfolderpath, planename, pics[i])
        picdata=read_pic_from_file(new_pic_file)
        picdata=normalize_data(picdata)
        data[i,:,:,:]=picdata
    return data

def read_n_images(planename,n):
    picfolder=pic_file = os.path.join(Inputfolderpath, planename)
    pics = os.listdir(picfolder)
    data = np.ndarray((n, pixels_lengthwise, pixels_depthwise, RGB_channels), dtype=np.float16)
    for i in range(0,n):
        new_pic_file = os.path.join(Inputfolderpath, planename, pics[i])
        picdata=read_pic_from_file(new_pic_file)
        picdata=normalize_data(picdata)
        data[i,:,:,:]=picdata
    return data


def Process_Image_to_Array():
    planetypes=os.listdir(Inputfolderpath)

    indices_array={}
    num_array={}
    num_train=0
    num_val=0
    num_test=0
    for no, planetype in enumerate(planetypes):
        num_pics=len(os.listdir(Inputfolderpath+planetype))
        plane_num_val=int(np.floor(frac_val*num_pics))
        plane_num_test=int(np.floor(frac_test*num_pics))
        plane_num_train=num_pics-plane_num_val-plane_num_test
        indices_array[planetype]=[0, plane_num_train, plane_num_train+plane_num_val, plane_num_train+plane_num_val+plane_num_test]
        num_array[planetype]=[plane_num_train, plane_num_val, plane_num_test]
        num_train=num_train+plane_num_train
        num_val=num_val+plane_num_val
        num_test=num_test+plane_num_test
        print('Number of ', planetype, ':', str(num_pics))
        print('Train: %i, Val: %i, Test: %i' % (plane_num_train, plane_num_val, plane_num_test))
        #print(indices_array[planetype])
    print('TOTALS')
    print('Train: %i, Val: %i, Test: %i' % (num_train, num_val, num_test))

    #train_data, train_labels=make_dataset_arrays(test_size*3, 3)
    train_data, train_labels=make_dataset_arrays(num_train, no+1)
    val_data, val_labels=make_dataset_arrays(num_val, no+1)
    test_data, test_labels=make_dataset_arrays(num_test, no+1)

    current_train_index=0
    current_val_index=0
    current_test_index=0
    for no, planetype in enumerate(planetypes):
        t1 = time.time()
        print('Processing ', planetype)
        planedata=read_n_images(planetype, indices_array[planetype][3])
        train_data[current_train_index:current_train_index+num_array[planetype][0],:,:,:]=planedata[indices_array[planetype][0]:indices_array[planetype][1],:,:,:]
        train_labels[current_train_index:current_train_index+num_array[planetype][0],no]=np.ones(num_array[planetype][0])
        val_data[current_val_index:current_val_index+num_array[planetype][1],:,:,:]=planedata[indices_array[planetype][1]:indices_array[planetype][2],:,:,:]
        val_labels[current_val_index:current_val_index+num_array[planetype][1],no]=np.ones(num_array[planetype][1])
        test_data[current_test_index:current_test_index+num_array[planetype][2],:,:,:]=planedata[indices_array[planetype][2]:indices_array[planetype][3],:,:,:]
        test_labels[current_test_index:current_test_index+num_array[planetype][2],no]=np.ones(num_array[planetype][2])
        current_train_index+=num_array[planetype][0]
        current_val_index+=num_array[planetype][1]
        current_test_index+=num_array[planetype][2]
        t2 = time.time()
        print("Processing Time:", t2 - t1)

    train_data, train_labels =shuffle_data(train_data, train_labels)
    val_data, val_labels =shuffle_data(val_data, val_labels)
    test_data, test_labels =shuffle_data(test_data,test_labels)

    pickle_file = 'airplane_data_downsample.pickle'
    # save = {
    #     'test_data': test_data,
    #     'test_labels': test_labels}
    save = {
        'train_data': train_data,
        'train_labels': train_labels,
        'val_data': val_data,
        'val_labels': val_labels,
        'test_data': test_data,
        'test_labels': test_labels}
    try:
        f = open(Outputfolderpath + pickle_file, 'wb')
        pck.dump(save, f, pck.HIGHEST_PROTOCOL)
        f.close()
    except Exception as e:
        print('Unable to save data to', pickle_file, ':', e)
        raise






if __name__=='__main__':
    print('Input Folder: ', os.path.abspath(Inputfolderpath))
    print('Output Folder: ', os.path.abspath(Outputfolderpath))
    #print("%x" % sys.maxsize, sys.maxsize > 2 ** 32)
    starttime = time.time()
    Process_Image_to_Array()
    endtime = time.time()
    print("TOTAL Processing Time:", endtime - starttime)