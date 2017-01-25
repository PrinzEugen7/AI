# -*- coding: utf-8 -*-
from sklearn import datasets
from sklearn.externals import joblib

def main():
    # データセットを読み込み（アイリス）
    iris = datasets.load_iris()
    # 予測モデルを復元
    clf = joblib.load('svm.learn') 
    # 予測結果を出力
    print(clf.predict(iris.data))

if __name__ == "__main__":
    main()
