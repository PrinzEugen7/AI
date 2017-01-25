# -*- coding: utf-8 -*-
from skimage import io
from skimage.color import*
 
def main():
    img = io.imread('test.jpg')
    hsv = rgb2hsv(img)
    io.imshow(hsv)
    
if __name__ == "__main__":
    main()
