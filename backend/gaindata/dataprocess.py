import os
import json

TOPIC = 'RUS_UKR'
ROOT_PATH = '../../preprocessv2/datasets/mergesets/' + TOPIC +'/'

MEDIA_XY = '../../preprocessv2/datasets/mediaxy/doctone_results.json'
MEDIA_NUMS = '../../preprocessv2/datasets/mediaxy/media_nums.json'


def fuctionA():
    pass


def mediaDataSet():
    # print(os.listdir(ROOT_PATH))
    timerange = timeRange()
    media = meidaList()
    result = {
        'topic': TOPIC,
        'timerange': timerange,
        'media': media[0],
        'media_nums': media[1],
        'details': media[2]
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
        result.append(tdic)
    return result