from sklearn import datasets # データ・セット
from sklearn import svm

def main():
    # データ・セットを呼び出す
    digits = datasets.load_digits()
    # 教師データ
    target = digits.target[:-1]
    # サポートベクターマシンで教師あり学習
    clf = svm.SVC(gamma=0.001, C=100.)
    clf.fit(digits.data[:-1], digits.target[:-1])  
    print(clf)

if __name__ == "__main__":
    main()
