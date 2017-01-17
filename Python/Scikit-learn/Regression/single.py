# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn import linear_model

def main():
    data = pd.read_csv("data.csv", sep=",")
    clf = linear_model.LinearRegression()
    # 説明変数に "x1"のデータを使用
    X = data.loc[:, ['x1']].as_matrix()
    # 目的変数に "x2"のデータを使用
    Y = data['x2'].as_matrix()
    # 予測モデルを作成（単回帰）
    clf.fit(X, Y)
    # 回帰係数と切片の抽出
    [a] = clf.coef_
    b = clf.intercept_  
    # 回帰係数
    print("回帰係数:", a)
    print("切片:", b) 
    print("決定係数:", clf.score(X, Y))

if __name__ == "__main__":
    main()
