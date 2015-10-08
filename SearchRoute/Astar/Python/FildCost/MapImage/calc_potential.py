# -*- coding: utf-8 -*-
import numpy as np

def unique2d(a):
    x = np.array([a[0]])
    for i in xrange(a.shape[0]):
        if np.sum(a[i] - a[i-1]) != 0:
            x = np.append(x, [a[i]], axis=0)
    return np.delete(x, 1, 0)

def main():
    robo = np.loadtxt("robot1-0-0.csv")
    x,y,z = unique2d(robo).T
    w = np.loadtxt("wall.csv")
    o = np.loadtxt("obst.csv")
    b, Uo, Uw = 1, 0, 0
    # 壁のポテンシャルを計算
    for i in xrange(w.shape[0]):
        Uw += b/np.sqrt((w[i][0]-x)**2+(w[i][1]-y)**2)

    for i in xrange(o.shape[0]):
        Uo += b/np.sqrt((o[i][0]-x)**2+(o[i][1]-y)**2)

    U = Uw + Uo
    L = np.sum(np.sqrt(np.diff(x)**2+np.diff(y)**2))
    # 各ポテンシャルの重ねあわせ
    print("Uw=" + str(np.sum(Uw)) )
    print("uw=" + str(np.sum(Uw)/Uw.shape[0]) )
    print("Uo=" + str(np.sum(Uo)) )
    print("uo=" + str(np.sum(Uo)/Uo.shape[0]) )
    print("U=" + str(np.sum(U)) )
    print("u=" + str(np.sum(U)/U.shape[0]) )
    print("L=" + str(L) )

if __name__ == '__main__':
    main()
