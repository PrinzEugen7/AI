# -*- coding: utf-8 -*-
from skimage import io
from skimage.color import rgb2gray
 
def main():
    img = io.imread('test.jpg')
    gray = rgb2gray(img)
    io.imshow(gray)
    
if __name__ == "__main__":
    main()
