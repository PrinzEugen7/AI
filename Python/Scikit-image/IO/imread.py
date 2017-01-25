# -*- coding: utf-8 -*-
from skimage import io

def main():
    # CSVファイルを取得
    img = io.imread('test.jpg')
    io.imshow(img)
    
if __name__ == "__main__":
    main()
