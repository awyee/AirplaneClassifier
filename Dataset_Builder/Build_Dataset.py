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

def shuffle_files(files):
    random.shuffle(files)
    return files

def shuffle_data(data, labels):
    permutation = np.random.permutation(labels.shape[0])
    shuffled_dataset = data[permutation, :, :, :]
    shuffled_labels = labels[permutation, :]
    return shuffled_dataset, shuffled_labels

# def read100images(planename):
#     picfolder=pic_file = os.path.join(Inputfolderpath, planename)
#     pics = os.listdir(picfolder)
#     data = np.ndarray((test_size, pixels_lengthwise, pixels_depthwise, RGB_channels), dtype=np.float16)
#     for i in range(0,test_size):
#         new_pic_file = os.path.join(Inputfolderpath, planename, pics[i])
#         picdata=read_pic_from_file(new_pic_file)
#         picdata=normalize_data(picdata)
#         data[i,:,:,:]=picdata
#     return data

def read_n_images(planename,n):
    picfolder = os.path.join(Inputfolderpath, planename)
    pics = os.listdir(picfolder)
    data = np.ndarray((n, pixels_lengthwise, pixels_depthwise, RGB_channels), dtype=np.float16)
    for i in range(0,n):
        new_pic_file = os.path.join(Inputfolderpath, planename, pics[i])
        picdata=read_pic_from_file(new_pic_file)
        picdata=normalize_data(picdata)
        data[i,:,:,:]=picdata
    return data

def read_images_from_filenames(planename, filenames):
    data = np.ndarray((len(filenames), pixels_lengthwise, pixels_depthwise, RGB_channels), dtype=np.float16)
    for i,filename in enumerate(filenames):
        new_pic_file = os.path.join(Inputfolderpath, planename, filename)
        picdata=read_pic_from_file(new_pic_file)
        picdata=normalize_data(picdata)
        data[i,:,:,:]=picdata
    return data


def Process_Image_to_Array():
    planetypes=os.listdir(Inputfolderpath)

    indices_array={}
    num_array={}
    file_array={}
    min_length=9999999999
    num_train=0
    num_val=0
    num_test=0
    for no, planetype in enumerate(planetypes):
        file_array[planetype]=[jpg for jpg in os.listdir(Inputfolderpath + planetype) if 'jpg' in jpg]
        file_array[planetype]=shuffle_files(file_array[planetype])
        num_pics=len(file_array[planetype])
        min_length=np.min([num_pics, min_length])

        # plane_num_val=int(np.floor(frac_val*num_pics))
        # plane_num_test=int(np.floor(frac_test*num_pics))
        # plane_num_train=num_pics-plane_num_val-plane_num_test
        #
        # indices_array[planetype]=[0, plane_num_train, plane_num_train+plane_num_val, plane_num_train+plane_num_val+plane_num_test]
        # num_array[planetype]=[plane_num_train, plane_num_val, plane_num_test]
        #
        # num_train=num_train+plane_num_train
        # num_val=num_val+plane_num_val
        # num_test=num_test+plane_num_test

        print('Number of ', planetype, ':', str(num_pics))
        # print('Train: %i, Val: %i, Test: %i' % (plane_num_train, plane_num_val, plane_num_test))
        # print(indices_array[planetype])
    #print('Train: %i, Val: %i, Test: %i' % (num_train, num_val, num_test))

    #train_data, train_labels=make_dataset_arrays(test_size*3, 3)
    num_val_per_plane=int(np.floor(frac_val*min_length))
    num_val=num_val_per_plane*(no+1)
    num_test_per_plane=int(np.floor(frac_test*min_length))
    num_test=num_test_per_plane*(no+1)
    num_train_per_plane=int(min_length)-num_val_per_plane-num_test_per_plane
    num_train = num_train_per_plane*(no+1)
    # train_data, train_labels=make_dataset_arrays(num_train, no+1)
    val_data, val_labels=make_dataset_arrays(num_val, no+1)
    test_data, test_labels=make_dataset_arrays(num_test, no+1)
    print('TOTALS')
    print('Train: %i, Val: %i, Test: %i' % (num_train, num_val, num_test))


    # for no, planetype in enumerate(planetypes):
    #     t1 = time.time()
    #     print('Processing VAL and TEST for', planetype)
    #     val_data[(no)*num_val_per_plane:(no+1)*num_val_per_plane, :, :, :] = read_images_from_filenames(planetype,file_array[planetype][0:num_val_per_plane])
    #     val_labels[(no)*num_val_per_plane:(no+1)*num_val_per_plane, no] = np.ones(num_val_per_plane)
    #     test_data[(no)*num_test_per_plane:(no+1)*num_test_per_plane, :, :, :]= read_images_from_filenames(planetype,file_array[planetype][num_val_per_plane:num_val_per_plane+num_test_per_plane])
    #     test_labels[(no)*num_test_per_plane:(no+1)*num_test_per_plane, no] = np.ones(num_test_per_plane)
    #     t2 = time.time()
    #     print("Processing Time:", t2 - t1)
    #
    #
    # val_data, val_labels =shuffle_data(val_data, val_labels)
    # test_data, test_labels =shuffle_data(test_data,test_labels)
    #
    # pickle_file = 'airplane_VAL_AND_TEST.pickle'
    # # save = {
    # #     'test_data': test_data,
    # #     'test_labels': test_labels}
    # save = {
    #     'val_data': val_data,
    #     'val_labels': val_labels,
    #     'test_data': test_data,
    #     'test_labels': test_labels}
    # try:
    #     f = open(Outputfolderpath + pickle_file, 'wb')
    #     pck.dump(save, f, pck.HIGHEST_PROTOCOL)
    #     f.close()
    #     print('Saved val and test data to', pickle_file)
    # except Exception as e:
    #     print('Unable to save data to', pickle_file, ':', e)
    #     raise

    current_idx=num_val_per_plane+num_test_per_plane
    for i in range(0,int(np.ceil(num_train_per_plane/pickle_batch_size))):
    #jhfgmn     ,M ,MG  ,,for i in range (0,2):
        batch_size=np.min([pickle_batch_size,min_length-current_idx])
        train_data, train_labels=make_dataset_arrays(batch_size*(no+1), no+1)
        for no, planetype in enumerate(planetypes):
            t1 = time.time()
            print('Processing TRAIN %2d for' % i, planetype)
            train_data[(no)*batch_size:(no+1)*batch_size, :, :, :]= read_images_from_filenames(planetype,file_array[planetype][current_idx:current_idx+batch_size])
            train_labels[(no)*batch_size:(no+1)*batch_size, no] = np.ones(batch_size)
            t2 = time.time()
            print("Processing Time:", t2 - t1)
        train_data, train_labels = shuffle_data(train_data, train_labels)
        pickle_file = 'airplane_TRAIN_%2d.pickle' % i
        save = {
            'train_data_%2d' % i: train_data,
            'train_labels_%2d' % i: train_labels}
        try:
            f = open(Outputfolderpath + pickle_file, 'wb')
            pck.dump(save, f, pck.HIGHEST_PROTOCOL)
            f.close()
            print('Saved train data %2d to' % i, pickle_file)
        except Exception as e:
            print('Unable to save data to', pickle_file, ':', e)
            raise
        current_idx+=pickle_batch_size





if __name__=='__main__':
    print('Input Folder: ', os.path.abspath(Inputfolderpath))
    print('Output Folder: ', os.path.abspath(Outputfolderpath))
    #print("%x" % sys.maxsize, sys.maxsize > 2 ** 32)
    starttime = time.time()
    Process_Image_to_Array()
    endtime = time.time()
    print("TOTAL Processing Time:", endtime - starttime)