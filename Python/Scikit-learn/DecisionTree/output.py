# -*- coding: utf-8 -*-
import pandas as pd
from sklearn import tree

def main():
    # CSVファイルを取得
    data = pd.read_csv("data.csv", sep=",")
    # 説明変数(x1, x2に設定)
    variables = ['x1', 'x2']
    # 決定木の分類器を生成
    clf = tree.DecisionTreeClassifier()
    # 分類器にサンプルデータを入れて学習(目的変数はx）
    clf = clf.fit(data[variables], data['x3'])
    # 学習結果を出力
    with open('graph.dot', 'w') as f:
        f = tree.export_graphviz(clf, out_file=f)
        
if __name__ == "__main__":
    main()
