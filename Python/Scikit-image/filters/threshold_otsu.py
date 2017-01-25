# -*- coding: utf-8 -*-
from skimage import io
from skimage.color import*
from skimage.filters import threshold_otsu

def main():
    img = io.imread('test.jpg')
    gray = rgb2gray(img)
    th = threshold_otsu(gray)
    io.imshow(th)
    
if __name__ == "__main__":
    main()
