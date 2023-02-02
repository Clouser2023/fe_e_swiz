""" This script uses code originally written by CherishingWish @ https://github.com/CherishingWish """

from PIL import Image
import numpy as np
import sys

def swap(img, first, second):
    temp = img[first[0]:first[1], first[2]:first[3]].copy()
    img[first[0]:first[1], first[2]:first[3]] = img[second[0]:second[1], second[2]:second[3]]
    img[second[0]:second[1], second[2]:second[3]] = temp


def getblock(data):
    block1 = data[0:8, 0:8]
    block2 = data[0:8, 8:16]
    block3 = data[0:8, 16:24]
    block4 = data[0:8, 24:32]

    newblock = np.vstack((np.hstack((block2, block4)), np.hstack((block1, block3))))
    return newblock

def getbigblock(data):
    block1 = getblock(data[0:8, 0:32])
    block2 = getblock(data[0:8, 32:64])
    block3 = getblock(data[0:8, 64:96])
    block4 = getblock(data[0:8, 96:128])

    newblock = np.vstack((np.vstack((block4, block3)), np.vstack((block2, block1))))
    
    return newblock

def combinelineblock2048(data):
    block1 = getbigblock(data[0:8, 0:128])
    block2 = getbigblock(data[0:8, 128:256])
    block3 = getbigblock(data[0:8, 256:384])
    block4 = getbigblock(data[0:8, 384:512])
    block5 = getbigblock(data[0:8, 512:640])
    block6 = getbigblock(data[0:8, 640:768])
    block7 = getbigblock(data[0:8, 768:896])
    block8 = getbigblock(data[0:8, 896:1024])

    block9 = getbigblock(data[0:8, 1024:1152])
    block10 = getbigblock(data[0:8, 1152:1280])
    block11 = getbigblock(data[0:8, 1280:1408])
    block12 = getbigblock(data[0:8, 1408:1536])
    block13 = getbigblock(data[0:8, 1536:1664])
    block14 = getbigblock(data[0:8, 1664:1792])
    block15 = getbigblock(data[0:8, 1792:1920])
    block16 = getbigblock(data[0:8, 1920:2048])

    newblock_1 = np.vstack((np.hstack((block3, block4)), np.hstack((block1, block2))))
    newblock_2 = np.vstack((np.hstack((block7, block8)), np.hstack((block5, block6))))

    newblock_3 = np.vstack((np.hstack((block11, block12)), np.hstack((block9, block10))))
    newblock_4 = np.vstack((np.hstack((block15, block16)), np.hstack((block13, block14))))

    newblock = np.vstack((np.vstack((newblock_4, newblock_3)), np.vstack((newblock_2, newblock_1))))

    return newblock

def combinelineblock1024(data):
    block1 = getbigblock(data[0:8, 0:128])
    block2 = getbigblock(data[0:8, 128:256])
    block3 = getbigblock(data[0:8, 256:384])
    block4 = getbigblock(data[0:8, 384:512])
    block5 = getbigblock(data[0:8, 512:640])
    block6 = getbigblock(data[0:8, 640:768])
    block7 = getbigblock(data[0:8, 768:896])
    block8 = getbigblock(data[0:8, 896:1024])

    newblock_1 = np.vstack((np.hstack((block3, block4)), np.hstack((block1, block2))))
    newblock_2 = np.vstack((np.hstack((block7, block8)), np.hstack((block5, block6))))

    newblock = np.vstack((newblock_2, newblock_1))

    return newblock

def combinelineblock512(data):
    block1 = getbigblock(data[0:8, 0:128])
    block2 = getbigblock(data[0:8, 128:256])
    block3 = getbigblock(data[0:8, 256:384])
    block4 = getbigblock(data[0:8, 384:512])

    newblock = np.vstack((np.hstack((block3, block4)), np.hstack((block1, block2))))

    return newblock

def combineVblock(data,dimension=2048):
    if dimension==2048:
        block1 = combinelineblock2048(data[0:8, 0:2048])
        block2 = combinelineblock2048(data[8:16, 0:2048])
        block3 = combinelineblock2048(data[16:24, 0:2048])
        block4 = combinelineblock2048(data[24:32, 0:2048])
        newblock = np.hstack((np.vstack((block3, block4)), np.vstack((block1, block2))))
    elif dimension==1024:
        block1 = combinelineblock1024(data[0:8, 0:1024])
        block2 = combinelineblock1024(data[8:16, 0:1024])
        block3 = combinelineblock1024(data[16:24, 0:1024])
        block4 = combinelineblock1024(data[24:32, 0:1024])
        newblock = np.vstack((np.vstack((block1, block2)), np.vstack((block3, block4))))
    elif dimension==512:
        block1 = combinelineblock512(data[0:8, 0:512])
        block2 = combinelineblock512(data[8:16, 0:512])
        block3 = combinelineblock512(data[16:24, 0:512])
        block4 = combinelineblock512(data[24:32, 0:512])
        newblock = np.vstack((np.vstack((block1, block2)), np.vstack((block3, block4))))
    
    return newblock

def unswizzleImage(image_array):
    replace = temp.copy()
    dim = temp.shape[0]
    if dim==2048:
        for j in range(1024):
            if j % 32 == 0:
                block1 = combineVblock(temp[j:j+32, 0:2048])
                block2 = combineVblock(temp[1024+j:1024+j+32, 0:2048])
                block = np.vstack((block1, block2))

                replace[0:2048, 2048-j*2-64:2048-j*2] = block
    else:
        for j in range(int(dim)):
            if j % 32 == 0:
                block = combineVblock(temp[j:j+32,0:dim],dim)

                replace[0:dim, dim-j-32:dim-j] = block

    return replace
        

file_paths = sys.argv[1:]

for i in file_paths:

    print("Image: " + i)

    name = i
    image = Image.open(name)

    temp = np.asarray(image)
    temp = temp.copy()
    temp.setflags(write=1)

    if temp.shape[0] not in [512,1024,2048] or temp.shape[0]!=temp.shape[1]:
        print("Unsopported image size, skipping image.")
        continue

    replace = unswizzleImage(temp)          

    image = Image.fromarray(replace)
    n = i.split(".")
    
    image.save(n[0]+"_unswizzled."+n[1])
