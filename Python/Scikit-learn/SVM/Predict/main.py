from sklearn import datasets # データ・セット
from sklearn import svm
from sklearn import metrics
    
def main():
    # データ・セットを呼び出す
    digits = datasets.load_digits()
    data = digits.data[:-1]
    # 教師データ(正解データ)
    expected = digits.target[:-1]
    # サポートベクターマシンで教師あり学習
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(data, expected)

    # 作成した分類器でデータを分類(推定)
    predicted = clf.predict(data)

    # 分類結果(正答率やF値など)を表示
    print("Classification report for classifier %s:\n%s\n"
      % (clf, metrics.classification_report(expected, predicted)))
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))
    
if __name__ == "__main__":
    main()
