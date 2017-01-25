# -*- coding: utf-8 -*-
from sklearn import svm
from sklearn import datasets
from sklearn.externals import joblib

def main():
    # データセットの読み込み(アイリス)
    iris = datasets.load_iris()
    clf = svm.SVC()
    # データセットから目的変数と説明変数を取り出す
    X, y = iris.data, iris.target
    # 予測
    clf.fit(X, y)
    # 予測結果をコンソールに出力
    print(clf.predict(X))
    # 予測モデルを出力
    joblib.dump(clf, 'svm.learn') 

if __name__ == "__main__":
    main()
