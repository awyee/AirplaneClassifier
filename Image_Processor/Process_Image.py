from PIL import Image
import os
import numpy as np
import time



Inputfolderpath='../../Pics/Raw/'
Outputfolderpath='../../Pics/Processed_downsampled/'
planetypes = os.listdir(Inputfolderpath)
RGB_channels=3
frac_val=0.2
frac_test=0.1
Padded_Height=400
Padded_Width=400

def read_pic_from_file(file_path):
    img = Image.open(file_path)
    if img.size[0]>img.size[1]:
        resize_width=Padded_Width
        resize_height=int(np.ceil(img.size[1]*Padded_Width/img.size[0]))
    else:
        resize_height=Padded_Height
        resize_width=int(np.ceil(img.size[0]*Padded_Height/img.size[1]))

    img = img.resize((resize_width,resize_height), Image.ANTIALIAS)  # downsample image
    pixel_values = np.array(img.getdata()).reshape(img.size[1], img.size[0], 3)
    pixel_values=trimbanner(pixel_values,img.size)
    pixel_values=padimage(pixel_values)
    return pixel_values

def trimbanner(pixel_values,imgsize):
    droprowfound = False
    droprow = imgsize[1]
    maxcol = imgsize[0] - 1
    mid = int(np.floor(maxcol / 2))
    oneqtr = int(np.floor(maxcol / 4))
    threeqtr = int(np.floor(maxcol * 3 / 4))
    while droprowfound == False:
        droprow = droprow - 1
        test = np.sum(pixel_values[droprow, oneqtr, :]) + np.sum(pixel_values[droprow, mid, :]) + np.sum(
            pixel_values[droprow, threeqtr, :])
        if test >= 100:
            droprowfound = True
    return pixel_values[0:droprow, :, :]

def padimage(pic):
    curr_shape = pic.shape
    pad_top = np.zeros([int(np.floor((Padded_Height - curr_shape[0]) / 2)), curr_shape[1], 3])
    pad_bot = np.zeros([int(np.ceil((Padded_Height - curr_shape[0]) / 2)), curr_shape[1], 3])
    pad_left = np.zeros([Padded_Height, int(np.floor((Padded_Width - curr_shape[1]) / 2)), 3])
    pad_right = np.zeros([Padded_Height, int(np.ceil((Padded_Width - curr_shape[1]) / 2)), 3])
    added_top = np.append(pad_top, pic, axis=0)
    added_bot = np.append(added_top, pad_bot, axis=0)
    added_left = np.append(pad_left, added_bot, axis=1)
    padded_array = np.append(added_left, pad_right, axis=1)
    return padded_array

indices_array = {}
num_train = 0
num_val = 0
num_test = 0
starttime = time.time()
for no, planetype in enumerate(planetypes):
    num_pics = len(os.listdir(Inputfolderpath + planetype + '/full'))
    plane_num_val = np.floor(frac_val * num_pics)
    plane_num_test = np.floor(frac_test * num_pics)
    plane_num_train = num_pics - plane_num_val - plane_num_test
    indices_array[planetype] = [0, plane_num_train, plane_num_train + plane_num_val,
                                plane_num_train + plane_num_val + plane_num_test]
    num_train = num_train + plane_num_train
    num_val = num_val + plane_num_val
    num_test = num_test + plane_num_test
    print('Number of ', planetype, ':', str(num_pics))
    print('Train: %i, Val: %i, Test: %i' % (plane_num_train, plane_num_val, plane_num_test))
    # print(indices_array[planetype])

    picfolder=os.path.normpath(os.path.abspath(Inputfolderpath) +'/'+ planetype + '/full')
    processedpicfolder = os.path.normpath(os.path.abspath(Outputfolderpath) + '/' + planetype)
    print(picfolder)
    pics = os.listdir(picfolder)

    num_images = 0
    t1 = time.time()

    #for picnum in range(0,10):
    for pic in pics:
        pic_file = os.path.join(picfolder, pic)
        #pic_file = os.path.join(picfolder, pics[picnum])
        try:
            pic_data = read_pic_from_file(pic_file)
            new_pic = Image.fromarray(np.uint8(pic_data), mode='RGB')
            new_pic_file = os.path.join(processedpicfolder, pic)
            #new_pic_file = os.path.join(processedpicfolder, pics[picnum])
            new_pic.save(new_pic_file)
            num_images = num_images + 1
        except IOError as e:
            print('Could not read:', pic_file, ':', e)
    t2 = time.time()
    print("Processing Time:", t2 - t1)
endtime = time.time()
print("TOTAL Processing Time:", endtime - starttime)