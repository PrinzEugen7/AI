# -*- coding: utf-8 -*-
import scipy as sp
import numpy as np
from scipy import linalg as LA
import os
import glob
import ConfigParser

# 環境設定ファイル読込処理
envFile = ConfigParser.SafeConfigParser()
envFile.read(r'\horse\conf\config.ini')

horse_data_file_path = envFile.get('horse_data', 'file_path')

# 天候・馬場
weatherDict = {}
weatherIndex = 0

# 開催地
locationDict = {}
locationIndex = 0

# 馬データの読み込み
def loadHorseData(filename):
    horsedata = sp.genfromtxt(os.path.join(horse_data_file_path, filename), delimiter="\t", 
        dtype=[ ('日付','S10'),         # 0:日付
                ('開催地','i3'),       # 1:開催地
                ('レース','i2'),         # 2:レース 
                ('レース名','U50'),       # 3:レース名  
                ('距離','i4'),          # 4:距離  
                ('天候','i3'),         # 5:天候  
                ('馬番','i2'),          # 6:馬番 
                ('人気','i3'),          # 7:人気 
                ('着順','U10'),         # 8:着順 
                ('タイム','f5'),        # 9:タイム 
                ('差/事故', 'i4'),     # 10:差/事故  
                ('上3F','i4'),         # 11:上3F 
                ('通過順','U10'),      # 12:通過順
                ('体重','i4'),         # 13:体重
                ('騎手','U20'),        #　14:騎手
                ('負担重量','i4'),     # 15:負担重量
                ('調教師','U20'),      # 16:調教師
                ('獲得賞金（円）','U10')  # 17:獲得賞金
                ],                  
        converters={ 
            0 : lambda s: convertDate(s.decode('utf8')), # 開催日
            1 : lambda s: createLocationDict(s.decode('utf8')),    # 開催地
            3 : lambda s: s.decode('utf8'),    # レース名
            5 : lambda s: createWeatherDict(s.decode('utf8')),    # 天候
            9 : lambda s: convertTime(s.decode('utf8')), # タイム
            14 : lambda s: s.decode('utf8'),    # 騎手
            16: lambda s: s.decode('utf8'),    # 調教師
        })

    return np.array(horsedata.tolist(), dtype = object)

# １桁の場合は前ゼロを付与
def addZero(data):
    if len(data) == 2:
        return data
    else:
        return "0" + str(data)

def convertDate(date):
    aryYmd = date.split("/")
    year = addZero(aryYmd[0])
    month = addZero(aryYmd[1])
    day = addZero(aryYmd[2])
    return str(year) + str(month) + str(day)

def convertTime(time):
    if len(time.split(":")) == 2:
        return np.float32(time.split(":")[0])*60+np.float32(time.split(":")[1])
    else:
        return np.float32(time)
  
def createWeatherDict(weather):
    global weatherDict
    global weatherIndex
    
    if weatherDict.has_key(weather) == False:
        weatherIndex += 1
        weatherDict[weather] = weatherIndex
    return weatherDict[weather]
        
def createLocationDict(location):
    global locationDict
    global locationIndex
    
    if locationDict.has_key(location) == False:
        locationIndex += 1
        locationDict[location] = locationIndex
    return locationDict[location]
    
def paddingArray(ymd, loc, d, weather, n, y, w1, w2, padding):
    if padding.size != 0:
        y = y[padding]
        d = d[padding]
        w1 = w1[padding]
        w2 = w2[padding]
        n = n[padding]
        ymd = ymd[padding]
        weather = weather[padding]
        loc = loc[padding]
    return y, d, w1, w2, n, ymd, weather, loc
    
#　データを整形する。
def dataShaping(horsedata):
    ymd = horsedata[:,0] # 開催日の配列を作成
    loc = horsedata[:,1]  # 開催地の配列を生成
    d = horsedata[:,4]    # 距離の配列を生成
    weather = horsedata[:,5] # 天候の配列を生成
    n = horsedata[:,6]     # 馬番の配列を生成
    y = horsedata[:,9]    # タイムの配列を作成
    w1 = horsedata[:,13]  # 体重の配列を生成
    w2 = horsedata[:,15]  # 負担重量の配列を生成

    # 記録が無いレースを除外
    z = np.array([idx for idx, i in enumerate(y) if i == i  ])
    y, d, w1, w2, n, ymd, weather, loc = paddingArray(ymd, loc, d, weather, n, y, w1, w2, z)

    # 古い開催データを除外(2013より古いデータは除去）
    z = np.array([idx for idx, i in enumerate(ymd) if np.float32(i) >= np.float32(130101)])
    y, d, w1, w2, n, ymd, weather, loc = paddingArray(ymd, loc, d, weather, n, y, w1, w2, z)

    # .Tは転置
    return np.array([d, w1, w2, n, weather, ymd, np.ones(len(n))]).T, y

def getParam(filename):
  # 以下、main処理
    horsedata = loadHorseData(filename)
    x, y = dataShaping(horsedata)
    return LA.lstsq(x, y)[0]       # 偏回帰係数

def calctime(params, distance, weight1, weight2, no, ymd, weather):
    t = np.int32(distance) * params[0] + np.int32(weight1) * params[1] + np.int32(weight2) * params[2] + np.int32(no) * params[3] + np.int32(weather) * params[4] + np.int32(ymd) * params[5] + params[6]
    print "|" + str(no) + "|" + str(t) + "|"

    return t

# 8R
print "8R 1200m"
calctime(getParam(u"ウィークエンド.tsv"), 1200, 504, 54.0, 1, 150918, 11)
