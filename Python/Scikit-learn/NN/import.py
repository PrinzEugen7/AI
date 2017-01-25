# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.externals import joblib

def main():
    # データを取得
    data = pd.read_csv("data.csv", sep=",")
    # ニューラルネットで学習モデルを読み込み（復元）
    clf = joblib.load('nn.learn') 
    # 学習データを元に説明変数x1, x2から目的変数x3を予測
    pred = clf.predict(data[['x1', 'x2']])
    # 識別率を表示
    print (sum(pred == data['x3']) / len(data[['x1', 'x2']]))
    
if __name__ == "__main__":
    main()
