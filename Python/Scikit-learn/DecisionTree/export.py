# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import tree

def main():
    # CSVファイルを取得
    data = pd.read_csv("data.csv", sep=",")
    # 学習モデルの復元
    clf = joblib.load('tree.learn')
    # 学習した分類器で予測
    pred = clf.predict(data[['x1', 'x2']])
    # 予測結果を表示
    print (pred)
    # 識別率を表示
    print (sum(pred == data['x3']) / len(data[['x1', 'x2']]))
        
if __name__ == "__main__":
    main()
