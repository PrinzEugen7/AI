# -*- coding: utf-8 -*-
from heapq import heappush, heappop
import math
import time
import random

class node:
    xPos = 0 # x position
    yPos = 0 # y position
    distance = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate
    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        d = math.sqrt(xd * xd + yd * yd)
        return(d)

# A-star algorithm.
def pathFind(maps, (x1, y1), (x2, y2)):
    n=30
    m=30
    dirs = 8 # マップ上の移動可能な方向数
    dx = [1, 1, 0, -1, -1, -1, 0, 1]
    dy = [0, 1, 1, 1, 0, -1, -1, -1]
    closed_map = [] # 閉ノードのマップ
    open_map = [] # オープンノードのマップ
    dir_map = [] # 方向のマップ
    row = [0] * n
    for i in range(m): # 2次元リストの作成
        closed_map.append(list(row))
        open_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # 開始ノードを作成してオープンノードリストにプッシュ
    n0 = node(x1, y1, 0, 0)
    n0.updatePriority(x2, y2)
    heappush(pq[pqi], n0)
    open_map[y1][x1] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # オープンノードのリストから最も優先度の高いノードを取得
        n1 = pq[pqi][0] # トップのノード
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # オープンリストから
        open_map[y][x] = 0
        closed_map[y][x] = 1 # マーク

        # ゴールに到着したら探索終了
        if x == x2 and y == y2:
            # 経路作成
            path = ''
            while not (x == x1 and y == y1):
                j = dir_map[y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
                x += dx[j]
                y += dy[j]

            print('Path:',path)
            if len(path) > 0:
                (x, y) = (x1, y1)
                maps[y][x] = 2
                for i in range(len(path)):
                    j = int(path[i])
                    x += dx[j]
                    y += dy[j]
                    maps[y][x] = 3

            for y in range(m):
                 for x in range(n):
                    xy = maps[y][x]
                    if xy == 0:
                        print '.', # space
                    elif xy == 1:
                        print 'O', # obstacle
                    elif xy == 2:
                        print 'S', # start
                    elif xy == 3:
                        print 'R', # route
                 print

        # 移動可能な移動方向の作成（子ノード）
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or maps[ydy][xdx] == 1 or closed_map[ydy][xdx] == 1):
                # 子ノード
                m0 = node(xdx, ydy, n0.distance, n0.priority)
                m0.nextMove(dirs, i)
                m0.updatePriority(x2, y2)
                # オープンリスト中にない場合は追加
                if open_map[ydy][xdx] == 0:
                    open_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # 親ノードの方向をマーク
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                elif open_map[ydy][xdx] > m0.priority:
                    # 優先度を更新
                    open_map[ydy][xdx] = m0.priority
                    # 親の方向を更新
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # 目標ノードを除去
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # より良いノードを代入
    return 'No Route'

def main():
    maps = []
    row = [0] * 30
    for i in range(30): # create empty map
        maps.append(list(row))
    pathFind(maps, (1, 1), (20, 20))

if __name__ == "__main__":
    main()
