from matplotlib import pyplot as plt
from sklearn import datasets # データ・セット

def main():
    # Iris のデータを呼び出す
    iris = datasets.load_iris()
    X = iris.data[:, :2]  # 最初の二次元のみの特徴量を抽出
    Y = iris.target       # 目標値（正解データ）
    # グラフの軸幅
    x_min, x_max = X[:, 0].min() - .5, X[:, 0].max() + .5
    y_min, y_max = X[:, 1].min() - .5, X[:, 1].max() + .5
    # 可視化のベースを作成
    plt.figure(2, figsize=(8, 6))
    plt.clf()
    # 実際にプロット
    plt.scatter(X[:, 0], X[:, 1], c=Y, cmap=pl.cm.Paired)
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()
