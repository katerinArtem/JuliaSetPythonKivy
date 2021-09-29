from numba.core.target_extension import JitDecorator
import numpy as np
import time
import numba 
from numba import objmode
from PIL import Image
from numpy import random
import programm


# Image width and height; parameters for the plot
##im_width, im_height = 1000, 1000
##c = complex(-0.7, 0.75)
##zabs_max = 10.0
##nit_max = 500
xmin, xmax = -2, 2
xwidth = xmax - xmin
ymin, ymax = -2, 2
yheight = ymax - ymin



@numba.njit
def calc(start,c,zabs_max,nit_max,im_width,im_height)-> np.ndarray:
    julia = np.zeros((im_width, im_height,3),dtype=np.uint8)
    pos = 1
    for ix in range(im_width):
        if ix > im_width/100*pos:
            pos = pos + 1
            with objmode(time1='f8'):
                time1 = time.time()
            print(pos,"%","  time passed:",time1 - start,"  time left:",((time1 - start)/pos)*(100-pos))
        for iy in range(im_height):
            nit = 0
            z = complex(ix / im_width * xwidth + xmin,
                        iy / im_height * yheight + ymin)
            while abs(z) <= zabs_max and nit < nit_max:
                z = c*z*(1 - z)
                ##z = z*z + c
                nit += 1
            ##shade = 1-np.sqrt(nit / nit_max)
            ratio = nit / nit_max
            julia[ix,iy,0] = ratio*255
    return julia



def saveImage(path,c = complex(-0.7, 0.75),r = 10.0,n = 500,w = 500,h = 500) -> str:
    start = time.time()
    #############################################################
    array = calc(start,c,r,n,w,h)
    img = Image.fromarray(array, 'RGB').save(path)
    #############################################################
    end = time.time()
    print("time:",end - start)
    print("calculation completed")
    print("re:",c.real,"im:",c.imag)
    return path

def getImage() -> Image:
    start = time.time()
    #############################################################
    array = calc(start)
    img = Image.fromarray(array, 'RGB')
    #############################################################
    end = time.time()
    print("time:",end - start)
    print("calculation completed")
    return img

def getArray(c = complex(-0.7, 0.75),r = 10.0,n = 500,w = 500,h = 500):
    start = time.time()
    #############################################################
    array = calc(start,c,r,n,w,h)
    #############################################################
    end = time.time()
    print("time:",end - start)
    print("calculation completed")
    print("re:",c.real,"im:",c.imag)
    return array

