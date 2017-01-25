# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.externals import joblib

def main():
    clf = joblib.load('clf.learn')
    # 回帰係数と切片の抽出
    [a] = clf.coef_
    b = clf.intercept_  
    # 回帰係数
    print("回帰係数:", a)
    print("切片:", b) 

    
if __name__ == "__main__":
    main()
