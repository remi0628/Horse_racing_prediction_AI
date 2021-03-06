import json
import pprint
import datetime
import traceback
import numpy as np
import pandas as pd
from collections import OrderedDict
from datetime import datetime as dt

JSON_RACE = './55879.json'

def predict(race):
    with open(race, encoding="utf-8_sig") as f:
        race_json = json.load(f)
    today_data, today_data_horse = today_race(race_json)
    print(today_data)
    print(today_data_horse)
    latest_races(race_json, today_data, today_data_horse)
    #pprint.pprint(race_json['course_distance'], width=60)


# 当日データ
def today_race(race_json):
    today_data = {}
    today_data_horse = []
    race_data = race_json.copy()
    # コース詳細{date, place, type, r, distance, status}
    today_data['date'] = race_data['date']
    today_data['place'] = race_data['place']
    today_data['course_type'] = race_data['course_type']
    today_data['r'] = race_data['r']
    today_data['course_distance'] = race_data['course_distance']
    today_data['course_status'] = race_data['course_status']
    # 馬詳細
    number, weight, handicap, birthday, jockey, trainer = [], [], [], [], [], []
    #pprint.pprint(race_data['horses'][i]['weight'],  width=60) #p
    horse_cnt = len(race_data['horses'])
    for i in range(horse_cnt):
        number.append(i + 1)
        weight.append(race_data['horses'][i]['weight'])
        handicap.append(race_data['horses'][i]['handicap'])
        birthday.append(race_data['horses'][i]['horse']['birthday'])
        #jockey.append(race_data['horses'][i]['jockey'])
        #trainer.append(race_data['horses'][i]['horse']['trainer'])
    # list [cnt, number, weight, handicap, birthday]
    today_data_horse.append(horse_cnt)
    today_data_horse.append(number)
    today_data_horse.append(weight)
    today_data_horse.append(handicap)
    today_data_horse.append(birthday)
    #today_data_horse.append(jockey)
    #today_data_horse.append(trainer)
    return today_data, today_data_horse

def latest_races(race_json, today_data, today_data_horse):
    race_data = race_json.copy()
    #print(len(race_data['horses'][i]['latest_races']))
    horse_num = today_data_horse[0]
    for h in range(horse_num):
        race_data['horses'][h]['latest_races'].sort(key=lambda x: x['date'], reverse=True) # 日付降順

        df_ = pd.DataFrame(np.zeros((1, 30)), columns=["course_type", "R", "len", "soil_condition", "horse_cnt", "horse_number", "result_rank",
                                                                                 "weight", "borden_weight", "birth_days", "sec", "threeF", "corner_order_1", "corner_order_2", "corner_order_3",
                                                                                 "racecourse_urawa", "racecourse_funabashi", "racecourse_kawasaki", "racecourse_tokyo", "racecourse_nigata",
                                                                                 "racecourse_tyukei", "racecourse_ooi", "racecourse_hakodate", "racecourse_hanshin", "racecourse_nakayama",
                                                                                 "racecourse_kyoto", "racecourse_ogura", "racecourse_sapporo", "racecourse_fukushima", "racecourse_morioka"])
        dropList = []
        for i in range(13): # 一応12レース分まで取得
            try:
                # データで埋めた10レースまで取得
                if len(df_) > 9:
                    continue
                horse_id = race_data['horses'][h]['horse_id'] # 馬id
                if i == 0:
                    # 当日データ
                    course_status = today_data['course_status']
                    course_type = today_data['course_type']

                    r = today_data['r'].replace('R', '')
                    course_distance = today_data['course_distance'].replace('m', '')
                    horse_cnt = today_data_horse[0]
                    number = today_data_horse[1][h]
                    handicap = today_data_horse[3][h]
                    weight = today_data_horse[2][h]
                    today = dt.strptime(today_data['date'], '%Y-%m-%d')
                    birth_day = dt.strptime(today_data_horse[4][h], '%Y-%m-%d')
                    birthDate = today - birth_day
                    place = today_data['place']

                else:
                    # 過去データ
                    #print(race_data['horses'][h]['latest_races'][i-1]['horses'])
                    course_status = race_data['horses'][h]['latest_races'][i-1]['course_status']
                    course_type = race_data['horses'][h]['latest_races'][i-1]['course_type']

                    r = race_data['horses'][h]['latest_races'][i-1]['r'].replace('R', '')
                    course_distance = race_data['horses'][h]['latest_races'][i-1]['course_distance'].replace('m', '')
                    horse_cnt = len(race_data['horses'][h]['latest_races'][i-1]['horses'])
                    for n in range(horse_cnt): # 馬番
                        if race_data['horses'][h]['latest_races'][i-1]['horses'][n]['horse_id'] == horse_id:
                            number = race_data['horses'][h]['latest_races'][i-1]['horses'][n]['number']
                            num = n # 何番目の枠にデータがあるのか
                    handicap = race_data['horses'][h]['latest_races'][i-1]['horses'][n]['handicap']
                    weight = race_data['horses'][h]['latest_races'][i-1]['horses'][n]['weight']
                    today = dt.strptime(race_data['horses'][h]['latest_races'][i-1]['horses'][n]['date'], '%Y-%m-%d')
                    birth_day = dt.strptime(today_data_horse[4][h], '%Y-%m-%d')
                    birthDate = today - birth_day
                    place = race_data['horses'][h]['latest_races'][i-1]['place']

                    result_rank = race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_rank']
                    #print(race_data['horses'][h]['latest_races'][i-1]['horses'][n]['date'])
                    #print(race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_time'])
                    try:
                        m_s_f = datetime.timedelta(seconds=race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_time'])
                    except:
                        continue
                    threeF = race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_tf_time']
                    try:
                        corner_order_1 =  race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_corner_indexes'][0]
                    except:
                        corner_order_1 = 0
                    try:
                        corner_order_2 =  race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_corner_indexes'][1]
                    except:
                        corner_order_2 = 0
                    try:
                        corner_order_3 =  race_data['horses'][h]['latest_races'][i-1]['horses'][n]['res_corner_indexes'][2]
                    except:
                        corner_order_3 = 0


                # 馬場状態
                if course_status == '良':
                    df_.loc[i, 'soil_condition'] = course_status
                elif course_status == '稍':
                    df_.loc[i, 'soil_condition'] = course_status
                elif course_status == '重':
                    df_.loc[i, 'soil_condition'] = course_status
                elif course_status == '不':
                    df_.loc[i, 'soil_condition'] = course_status
                else:
                    df_.loc[i, 'soil_condition'] = course_status

                # コース種別
                if course_type == 'ダ':
                    df_.loc[i, 'course_type'] = course_type
                elif course_type == '芝':
                    df_.loc[i, 'course_type'] = course_type
                else:
                    df_.loc[i, 'course_type'] = course_type

                df_.loc[i, 'R'] = float(r)
                df_.loc[i, 'len'] = (float(course_distance))
                df_.loc[i, 'horse_cnt'] = float(horse_cnt)
                df_.loc[i, 'horse_number'] = float(number)
                df_.loc[i, 'borden_weight'] = float(handicap)
                df_.loc[i, 'birth_days'] = birthDate.days
                # 当日データはNoneがある
                try:
                    df_.loc[i, 'weight'] = float(weight)
                except:
                    df_.loc[i, 'weight'] = 0

                # 　競馬場
                df_.loc[i, 'racecourse_urawa'] = 1 if place == "浦和" else 0
                df_.loc[i, 'racecourse_funabashi'] = 1 if place == "船橋" else 0
                df_.loc[i, 'racecourse_kawasaki'] = 1 if place == "川崎" else 0
                df_.loc[i, 'racecourse_tokyo'] = 1 if place == "東京" else 0
                df_.loc[i, 'racecourse_nigata'] = 1 if place == "新潟" else 0
                df_.loc[i, 'racecourse_tyukei'] = 1 if place == "中京" else 0 # ここまで左回り
                df_.loc[i, 'racecourse_ooi'] = 1 if place == "大井" else 0
                df_.loc[i, 'racecourse_hakodate'] = 1 if place == "函館" else 0
                df_.loc[i, 'racecourse_hanshin'] = 1 if place == "阪神" else 0
                df_.loc[i, 'racecourse_nakayama'] = 1 if place == "中山" else 0
                df_.loc[i, 'racecourse_kyoto'] = 1 if place == "京都" else 0
                df_.loc[i, 'racecourse_ogura'] = 1 if place == "小倉" else 0
                df_.loc[i, 'racecourse_sapporo'] = 1 if place == "札幌" else 0
                df_.loc[i, 'racecourse_fukushima'] = 1 if place == "福島" else 0
                df_.loc[i, 'racecourse_morioka'] = 1 if place == "盛岡" else 0 # 左周り


                if i == 0:
                    # 当日データ
                    df_.loc[i, 'result_rank'] = 0
                    df_.loc[i, 'sec'] = 0
                    df_.loc[i, 'threeF'] = 0
                    df_.loc[i, 'corner_order_1'] = 0
                    df_.loc[i, 'corner_order_2'] = 0
                    df_.loc[i, 'corner_order_3'] = 0

                else:
                    df_.loc[i, 'result_rank'] = float(result_rank)
                    # 上3F（3ハロン）
                    try:
                        df_.loc[i, 'threeF'] = float(threeF)
                    except ValueError:
                        df_.loc[idx, 'threeF'] = 0

                    # タイム(秒)
                    try:
                        time = datetime.datetime.strptime(str(m_s_f), '%H:%M:%S.%f')
                        df_.loc[i, 'sec'] = float(time.minute * 60 + time.second + time.microsecond / 1000000)
                    except:
                        time = dt.strptime(str(m_s_f), '%H:%M:%S')
                        df_.loc[i, 'sec'] = float(time.minute * 60 + time.second + time.microsecond / 1000000)

                    # コーナー通過順
                    try:
                        df_.loc[i, 'corner_order_1'] = float(corner_order_1)
                    except:
                        df_.loc[i, 'corner_order_1'] = 0
                    try:
                        df_.loc[i, 'corner_order_2'] = float(corner_order_1)
                    except:
                        df_.loc[i, 'corner_order_2'] = 0
                    try:
                        df_.loc[i, 'corner_order_3'] = float(corner_order_3)
                    except:
                        df_.loc[i, 'corner_order_3'] = 0

            except: # エラーなら全部0
                traceback.print_exc()
                dropList.append(i)
                df_.loc[i] = 0

        for i in dropList:
            df_.drop(i, axis=0, inplace=True)

        while len(df_) < 10:
            df_.loc[len(df_) + len(dropList)] = 0

        pd.set_option('display.max_columns', 100)
        print(df_.head(15))

def inZeroOne(num):
    if num > 1:
        return 1
    elif num < 0:
        return 0
    else:
        return num


def main():
    predict(JSON_RACE)


if __name__ == '__main__':
    main()
