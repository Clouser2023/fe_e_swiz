""" This script uses code originally written by CherishingWish @ https://github.com/CherishingWish """

from PIL import Image
import numpy as np
import sys

def unblock(data):
    block1 = data[8:16,0:8]
    block2 = data[0:8,0:8]
    block3 = data[8:16,8:16]
    block4 = data[0:8,8:16]
    newblock = np.hstack((block1,block2,block3,block4))
    return newblock
    

def unbigblock(data):
    block1 = unblock(data[48:64,0:16])
    block2 = unblock(data[32:48,0:16])
    block3 = unblock(data[16:32,0:16])
    block4 = unblock(data[0:16,0:16])

    newblock = np.hstack((block1,block2,block3,block4))

    return newblock


def unlineblock2048(data):
    block1 = unbigblock(data[448:512,0:16])
    block2 = unbigblock(data[448:512,16:32])
    block3 = unbigblock(data[384:448,0:16])
    block4 = unbigblock(data[384:448,16:32])
    block5 = unbigblock(data[320:384,0:16])
    block6 = unbigblock(data[320:384,16:32])
    block7 = unbigblock(data[256:320,0:16])
    block8 = unbigblock(data[256:320,16:32])
    block9 = unbigblock(data[192:256,0:16])
    block10 = unbigblock(data[192:256,16:32])
    block11 = unbigblock(data[128:192,0:16])
    block12 = unbigblock(data[128:192,16:32])
    block13 = unbigblock(data[64:128,0:16])
    block14 = unbigblock(data[64:128,16:32])
    block15 = unbigblock(data[0:64,0:16])
    block16 = unbigblock(data[0:64,16:32])

    newblock = np.hstack((block1,block2,block3,block4,block5,
                          block6,block7,block8,block9,block10,
                          block11,block12,block13,block14,block15,block16))
    return newblock

def unlineblock1024(data):
    block9 = unbigblock(data[192:256,0:16])
    block10 = unbigblock(data[192:256,16:32])
    block11 = unbigblock(data[128:192,0:16])
    block12 = unbigblock(data[128:192,16:32])
    block13 = unbigblock(data[64:128,0:16])
    block14 = unbigblock(data[64:128,16:32])
    block15 = unbigblock(data[0:64,0:16])
    block16 = unbigblock(data[0:64,16:32])
    
    newblock = np.hstack((block9,block10,block11,block12,block13,
                          block14,block15,block16))

    return newblock
    
def unlineblock512(data):
    block13 = unbigblock(data[64:128,0:16])
    block14 = unbigblock(data[64:128,16:32])
    block15 = unbigblock(data[0:64,0:16])
    block16 = unbigblock(data[0:64,16:32])

    newblock = np.hstack((block13,block14,block15,block16))
    return newblock

def undoVblock(data,dimension=2048):
    if dimension==2048:
        block1 = unlineblock2048(data[0:512,32:64])
        block2 = unlineblock2048(data[512:1024,32:64])
        block3 = unlineblock2048(data[0:512,0:32])
        block4 = unlineblock2048(data[512:1024,0:32])
        newblock = np.vstack((block1,block2,block3,block4))
    elif dimension==1024:
        block1 = unlineblock1024(data[0:256,0:32])
        block2 = unlineblock1024(data[256:512,0:32])
        block3 = unlineblock1024(data[512:768,0:32])
        block4 = unlineblock1024(data[768:1024,0:32])
        newblock = np.vstack((block1,block2,block3,block4))
    elif dimension==512:
        block1 = unlineblock512(data[0:128,0:32])
        block2 = unlineblock512(data[128:256,0:32])
        block3 = unlineblock512(data[256:384,0:32])
        block4 = unlineblock512(data[384:512,0:32])
        newblock = np.vstack((block1,block2,block3,block4))

    return newblock

def swizzleImage(image_array):
    replace = temp.copy()
    dim = temp.shape[0]
    if dim==2048:
        for j in range(1024):
            if j % 32 == 0:
                block1 = undoVblock(temp[0:1024,2048-2*j-64:2048-2*j])
                block2 = undoVblock(temp[1024:2048,2048-2*j-64:2048-2*j])
                replace[j:32+j,0:2048] = block1
                replace[1024+j:1024+32+j,0:2048] = block2
    else:
        for j in range(int(dim)):
            if j % 32 == 0:
                block1 = undoVblock(temp[0:dim,dim-j-32:dim-j],dim)
                replace[j:j+32,0:dim] = block1
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

    replace = swizzleImage(temp)

    image = Image.fromarray(replace)
    n = i.split(".")
    
    image.save(n[0]+"_swizzled."+n[1])
        
