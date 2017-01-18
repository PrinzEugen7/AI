# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans

def main():
    # CSVファイルを取得
    data = pd.read_csv("data.csv")
    # Pandasデータフレームをnumpy配列に変換
    data2 = np.array([data['x1'].tolist(), data['x2'].tolist(), data['x3'].tolist()], np.int32)
    # numpy配列を転置
    data2 = data2.T
    # k-means法でクラスタ分析（クラスタ数は3）
    result = KMeans(n_clusters=3).fit_predict(data)
    # クラスタ番号0の各要素の平均値
    data['cluster_id'] = result
    print(data[data['cluster_id']==0].mean())
 
if __name__ == "__main__":
    main()
