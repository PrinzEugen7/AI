# -*- coding: utf-8 -*-
from heapq import heappush, heappop
import numpy as np
import cv2

class node:
    def __init__(self, xp, yp, gs, fs): # 初期値
        (self.x,self.y) = (xp, yp)
        (self.gs,self.fs) = (gs, fs)
    def __lt__(self, other):            # f*の比較
        return self.fs < other.fs
    def update_fs(self, xd, yd):        # f*(n)=g*(n)+h*(n)の更新
        self.fs = self.gs + self.hs(xd, yd) * 10
    def next_move(self):                # 斜め直進の代わりに高いg*を与える
        self.gs += 10
    def hs(self, xd, yd):
        return(np.sqrt((xd - self.x)**2 + (yd - self.y)**2))

# A-star algorithm.
def astar(maps, (x1, y1), (x2, y2)):
    (n, m) = maps.shape
    closed = np.zeros((n, m), dtype=np.int) # closeリスト用マップ
    opened = np.zeros((n, m), dtype=np.int) # openリスト用マップ
    v = np.zeros((n, m), dtype=np.int)      # 方向用マップ
    vx = [1, 0, -1, 0]
    vy = [0, 1, 0, -1]
    cost = [[], []]             # オープンリストのコスト
    ci = 0                      # インデックスのコスト
    n0 = node(x1, y1, 0, 0)     # 開始ノードを作成してオープンノードリストにプッシュ
    n0.update_fs = 0            # f*(0)=0
    heappush(cost[ci], n0)
    closed[y1][x1] = n0.fs      # mark it on the open nodes map

    while len(cost[ci]) > 0:
        # openリストから最もコストの高いノードを取得
        n1 = cost[ci][0]        # トップのノード
        n0 = node(n1.x, n1.y, n1.gs, n1.fs)
        (x, y) = (n0.x, n0.y)
        heappop(cost[ci])
        opened[y][x] = 0
        closed[y][x] = 1
        # ゴールに到着したら探索終了して経路取得
        if x == x2 and y == y2:
            paths = [[x1, y1]]
            while not (x == x1 and y == y1):
                j = v[y][x]
                x += vx[j]
                y += vy[j]
                paths.append([y,x])
            return paths[::-1]

        # 移動可能な移動方向の作成（子ノード）
        for i in range(4):
            (xx, yy) = (x + vx[i], y + vy[i])
            if not (xx < 0 or xx > n-1 or yy < 0 or yy > m - 1 or maps[yy][xx] == 1 or closed[yy][xx] == 1):
                m0 = node(xx, yy, n0.gs, n0.fs)     # 子ノード
                m0.next_move()                      # 次へ移動
                m0.update_fs(x2, y2)                # 優先度の更新
                # openリスト中にない場合は追加
                if opened[yy][xx] == 0:
                    opened[yy][xx] = m0.fs
                    heappush(cost[ci], m0)
                    v[yy][xx] = (i + 2) % 4         # 親ノードの方向をマーク
                elif opened[yy][xx] > m0.fs:
                    opened[yy][xx] = m0.fs          # 優先度を更新
                    v[yy][xx] = (i + 2) % 4         # 親の方向を更新
                    while not (cost[ci][0].x == xx and cost[ci][0].y == yy):
                        heappush(cost[1 - ci], cost[ci][0])
                        heappop(cost[ci])
                    heappop(cost[ci])                # 目標ノードを除去
                    # 小さい方に、より大きなサイズのプライオリティキューを空にする
                    if len(cost[ci]) > len(cost[1 - ci]):
                        ci = 1 - ci
                    while len(cost[ci]) > 0:
                        heappush(cost[1-ci], cost[ci][0])
                        heappop(cost[ci])
                    ci = 1 - ci
                    heappush(cost[ci], m0)           # より良いノードを代入

def main():
    im = cv2.imread("map.png")                  # 地図画像の取得
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # グレースケール変換
    gray[gray < 50] = 1                         # 経路探索用マップに変換(移動可能=0, 不可=1)
    gray[gray > 51] = 0
    path = astar(gray, (1, 1), (99, 99))        # A*アルゴリズムで経路探索
    if len(path)==0:
        print("No route")
        return 0
    for y, x in path[::]:                       # 探索した経路を画像に描く
        cv2.circle(im,(int(x),int(y)), 1, (15,20,215), 1)
    cv2.imwrite("map2.png",im)

if __name__ == "__main__":
    main()
