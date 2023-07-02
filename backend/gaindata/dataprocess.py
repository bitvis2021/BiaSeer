import os
import json
import pandas as pd
from utils.helper import create_date_range,saveDictoJson

TOPIC = 'RUS_UKR'
ROOT_PATH = '../../preprocessv2/datasets/mergesets/' + TOPIC +'/'
MEDIA_CONCAT = '../../preprocessv2/same_event/concat/'

MEDIA_XY = '../../preprocessv2/datasets/mediaxy/doctone_results.json'
MEDIA_NUMS = '../../preprocessv2/datasets/mediaxy/media_nums.json'

TIME_BINS = 54

def mediaDataSet():
    # print(os.listdir(ROOT_PATH))
    timerange = timeRange()
    media = meidaList()
    result = {
        'topic': TOPIC,
        'timerange': timerange,
        'media': media[0],
        'media_nums': media[1],
        'details': media[2],
        'topicCodeList': [str(ele + 1) for ele in range(20)]
    }
    return result

def timeRange():
    csvList = os.listdir(ROOT_PATH)
    return 'time-time' if len(csvList) == 0 else csvList[0].split('.')[0] + '-' + csvList[-1].split('.')[0]

def meidaList():
    with open(MEDIA_XY,'r',encoding='utf8')as fp:
        media_xy = json.load(fp)
    with open(MEDIA_NUMS,'r',encoding='utf8')as fp:
        media_nums = json.load(fp)
    details = mediaDitails(media_nums, media_xy)
    return [list(media_xy.keys()), len(media_xy), details]

def mediaDitails(media_nums, media_xy):
    result = []
    index = 0
    for key, value in media_xy.items():
        tdic = {}
        tdic['domain'] = key
        tdic['x1'] = value[0]
        tdic['x2'] = value[1]
        tdic['nums'] = media_nums[key]
        tdic['id'] = index
        index += 1
        tdic['doctone'] = getDocTone(key)
        tdic['docnums'] = getDocNums(key)
        result.append(tdic)
    return result

def getDocTone(domain):
    return getFeatureTrending(domain, 'doctone')

def getDocNums(domain):
    return getFeatureTrending(domain, 'docnums')

def getFeatureTrending(domain, feature):
    result = {}
    time_range = timeRange()
    if feature not in ['doctone', 'docnums']:
        return result
    
    if time_range == 'time-time':
        return result
    
    tsplit = time_range.split('-')
    date_list = create_date_range([int(tsplit[0]),int(tsplit[1])])


    tmp = pd.read_csv(MEDIA_CONCAT + domain + '.' + feature +'.csv')
    topicList = list(tmp.columns)
    
    for topic in topicList:
        # print(type(topic))
        tmp_topic = str(int(topic)+1)
        result[tmp_topic] = []
        for index, value in enumerate(tmp[topic].to_list()):
            if value >= 0:
                max_v = value
                min_v = 0
            else:
                max_v = 0
                min_v = value
            result[tmp_topic].append({'date': date_list[index], 'value': max_v, 'value1': min_v })
    
    return result




def mediaMatrixDataSet():
    result = []
    media = meidaList()[0]
    
    timeBins, timeBinsIndex = gainTimeBins()

    for mele in media:
        tmp = {'domain' : mele, 'values': []}
        for mtopic in [str(ele + 1) for ele in range(20)]:
            tmp['values'].append({'topic':mtopic, 'details': gainMediaTopicTimeBinsData(mele, mtopic, timeBins, timeBinsIndex)})
        
        result.append(tmp)
    return result

def gainTimeBins():
    result = []
    time_range = timeRange()
    
    if time_range == 'time-time':
        return result
    
    tsplit = time_range.split('-')
    date_list = create_date_range([int(tsplit[0]),int(tsplit[1])])
    step = int(len(date_list) / TIME_BINS)
    timeBins = [date_list[i : i + step] for i in range(0,len(date_list), step)]

    timeBinsIndex = [list(range(i,i + step)) for i in range(0,len(date_list), step)]
    # print(timeBinsIndex)
    # print(len(timeBinsIndex))
    return timeBins, timeBinsIndex


def gainMediaTopicTimeBinsData(mele, mtopic, timeBins, timeBinsIndex):
    result = []
    tmp = pd.read_csv(MEDIA_CONCAT + mele + '.' + 'doctone.csv')
    for index, time in enumerate(timeBins):
        value = sum(tmp.loc[timeBinsIndex[index][0]:timeBinsIndex[index][-1], str(int(mtopic) - 1)]) / len(time)
        result.append({'date0' : time[0], 'date1' : time[-1], 'value' : value })
    return result