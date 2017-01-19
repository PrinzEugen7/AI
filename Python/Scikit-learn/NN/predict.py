# -*- coding: utf-8 -*-
import pandas as pd
from sklearn.neural_network import MLPClassifier

def main():
    # データを取得
    data = pd.read_csv("data.csv", sep=",")
    # ニューラルネットで学習
    clf = MLPClassifier(solver="sgd",random_state=0,max_iter=10000)
    # 予測
    clf.fit(data[['x1', 'x2']], data['x3'])
    pred = clf.predict(data[['x1', 'x2']])
    # 結果表示
    print (pred)
    
if __name__ == "__main__":
    main()
