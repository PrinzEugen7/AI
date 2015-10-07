# -*- coding: utf-8 -*-
class Node(object):
    def __init__(self,x,y):
        self.pos    = (x,y)
        self.hs  = (x-self.goal[0])**2 + (y-self.goal[1])**2
        self.fs = 0
        self.owner  = None
        self.parent = None

    def isGoal(self):
        return self.goal == self.pos

class NodeList(list):
    def find(self, x,y):
        l = [t for t in self if t.pos==(x,y)]
        return l[0] if l != [] else None
    def remove(self,node):
        del self[self.index(node)]

def main():

    maps = [
    [0,0,0,0,0],
    [0,0,1,0,1],
    [0,1,0,0,0],
    [0,1,1,0,0],
    [0,0,0,0,0]
    ]
    w = 5
    h = 5
    #スタート位置とゴール位置を設定
    Node.start = (1,1)
    Node.goal = (4,3)

    # OpenリストとCloseリストを設定
    opens = NodeList()
    close = NodeList()
    start = Node(*Node.start)
    start.fs = start.hs
    opens.append(start)

    while(1):
        #Openリストが空になったら解なし
        if opens == []:
            print "There is no route until reaching a goal."
            exit(1);

        #Openリストからf*が最少のノードnを取得
        n = min(opens, key=lambda x:x.fs)
        opens.remove(n)
        close.append(n)

        #最小ノードがゴールだったら終了
        if n.isGoal():
            end_node = n
            break

        #f*() = g*() + h*() -> g*() = f*() - h*()
        n_gs = n.fs - n.hs

        #ノードnの移動可能方向のノードを調べる
        for v in ((1,0),(-1,0),(0,1),(0,-1)):
            x = n.pos[0] + v[0]
            y = n.pos[1] + v[1]
            #マップが範囲外または壁(O)の場合はcontinue
            if (0 < y < h and 0 < x < w and maps[y][x] == '1'):
                continue
            #移動先のノードがOpen,Closeのどちらのリストに格納されているか、または新規ノードなのかを調べる
            m = opens.find(x,y)
            dist = (n.pos[0]-x)**2 + (n.pos[1]-y)**2
            if m:                #移動先のノードがOpenリストに格納されていた場合、より小さいf*ならばノードmのf*を更新し、親を書き換え
                if m.fs > n_gs + m.hs + dist:
                    m.fs = n_gs + m.hs + dist
                    m.parent = n
            else:
                m = close.find(x,y)
                if m:
                    #移動先のノードがCloseリストに格納されていた場合、より小さいf*ならばノードmのf*を更新し、親を書き換えかつ、Openリストに移動する
                    if m.fs > n_gs + m.hs + dist:
                        m.fs = n_gs + m.hs + dist
                        m.parent_node = n
                        opens.append(m)
                        close.remove(m)
                else:
                    #新規ノードならばOpenリストにノードに追加
                    m = Node(x,y)
                    m.fs = n_gs + m.hs + dist
                    m.parent = n
                    opens.append(m)

    #endノードから親を辿っていくと、最短ルートを示す
    n = end_node.parent
    #print n.pos
    m = [[x for x in line] for line in maps]
    while(1):
        if n.parent == None:
            break
        m[n.pos[1]][n.pos[0]] = '+'
        n = n.parent

    print n
    #print "\n".join(["".join(x) for x in m])

if __name__ == "__main__":
    main()
