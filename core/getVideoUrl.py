# HTTP库
import requests
# 借助BeautifulSoup包解析
from bs4 import BeautifulSoup
# 处理JSON数据
import json
# 解析url
import urllib
from urllib.parse import urlparse
from urllib.parse import parse_qs
# 操作excel
import numpy as np
import pandas as pd 
# 处理时间
import time
# 文件操作
import os

# 根据url获得html文件
def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()  #如果状态不是200，引发异常
        r.encoding='utf-8' #无论原来用什么编码，都改成utf-8
        return r.text 
    except:
        return ""

# 根据时间戳获得8位日期字符串
# now：1618921546，时间戳
def getDateStr(now = int(time.time())):
    now_Array = time.localtime(now)
    # time.struct_time(tm_year=2021, tm_mon=4, tm_mday=20, tm_hour=11,
    # tm_min=13, tm_sec=36, tm_wday=1, tm_yday=110, tm_isdst=0)
    now_str = "%04d%02d%02d" % (now_Array.tm_year,now_Array.tm_mon,now_Array.tm_mday)
    return now_str
    # '20210420'

# 规范化文件夹名称，去掉空格、/ \ : * ? " < > |
# 同时，本项目以下划线作为分隔符，所以，文件夹名称中也不能有下划线
def NormalFloderName(name):
    charArray=[' ','/','\\',':','*','?','"','<','>','|','_']
    for char in charArray:
        name=name.replace(char, '')
    return name

# 根据收藏夹url获得收藏夹API的url
# fav_url：收藏夹url
# fav_url='https://space.bilibili.com/91724487/favlist?fid=204884287&ftype=create'
def getFavlistAPI_url(fav_url):
    # 解析url的query部分
    fav_url_query=urlparse(fav_url).query
    # 将query解析成字典
    fav_url_query_dict=parse_qs(fav_url_query)
    # {'fid': ['204884287'], 'ftype': ['create']}
    # 获得收藏夹url中的fid
    fav_url_query_fid=fav_url_query_dict["fid"]
    # ['204884287']

    # fav_API_url模板
    fav_API_url='https://api.bilibili.com/x/v3/fav/resource/list?media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    
    # 解析fav_API_url的query
    fav_API_url_query=urlparse(fav_API_url).query
    # 'media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    # 将fav_API_url的query解析成字典
    fav_API_url_dict=parse_qs(fav_API_url_query)
    # {'media_id': ['1055169787'], 'pn': ['1'], 'ps': ['20'], 'order': ['mtime'], 
    # 'type': ['0'], 'tid': ['0'], 'platform': ['web'], 'jsonp': ['jsonp']}
    
    # 将fav_API_url中的media_id修改成fid即可
    fav_API_url_dict["media_id"]=fav_url_query_fid
    # 将页码设置为1，便于从第1页往后遍历收藏夹的所有页
    fav_API_url_dict["pn"]=1
    # 按收藏时间排序
    fav_API_url_dict["order"]="mtime"

    # 将dict类型参数转化为query_string格式
    fav_API_url_query=urllib.parse.urlencode(fav_API_url_dict,doseq=True)
    # 'media_id=204884287&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    fav_API_url='https://api.bilibili.com/x/v3/fav/resource/list?'+fav_API_url_query

    # 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=204884287&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    return fav_API_url

# 根据UP主投稿空间url获得投稿空间API的url
# contri_url：UP主投稿空间url，contribution
# contri_url='https://space.bilibili.com/258150656/video?tid=0&page=2&keyword=&order=pubdate'
def getContriAPI_url(contri_url):
    # 解析url的pash部分
    contri_url_path=urlparse(contri_url).path
    # '/258150656/video'
    # 获得mid
    mid=contri_url_path.split('/')[1]
    # '258150656'

    # contri_API_url模板
    contri_API_url='https://api.bilibili.com/x/space/arc/search?mid=258150656&ps=30&tid=0&pn=2&keyword=&order=pubdate&jsonp=jsonp'
    
    # 解析contri_API_url的query
    contri_API_url_query=urlparse(contri_API_url).query
    # 'mid=258150656&ps=30&tid=0&pn=2&keyword=&order=pubdate&jsonp=jsonp'
    # contri_API_url的query解析成字典
    contri_API_url_dict=parse_qs(contri_API_url_query)
    # {'mid': ['258150656'], 'ps': ['30'], 'tid': ['0'], 'pn': ['2'], 'order': ['pubdate'], 'jsonp': ['jsonp']}
    
    # 修改API_url中的mid
    contri_API_url_dict["mid"]=mid
    # 将页码设置为1，便于从第1页往后遍历收藏夹的所有页
    contri_API_url_dict["pn"]=1
    # 按发布时间排序
    contri_API_url_dict["order"]='pubdate'

    # 将dict类型参数转化为query_string格式
    contri_API_url_query=urllib.parse.urlencode(contri_API_url_dict,doseq=True)
    # 'media_id=204884287&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    contri_API_url='https://api.bilibili.com/x/space/arc/search?'+contri_API_url_query
    # 'https://api.bilibili.com/x/space/arc/search?mid=258150656&ps=30&tid=0&pn=1&order=pubdate&jsonp=jsonp'
    return contri_API_url

# 根据收藏夹API的url，批量获得收藏夹视频的url
# API_url：API的url
# excelFolder：文件夹，用于存放包含视频url的excel表格文件
# API_url='https://api.bilibili.com/x/v3/fav/resource/list?media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
# beginTime：视频最早发布时间，默认值是'19700101'
# endTime：视频最迟发布时间，默认值是当前日期8位字符串
# getFavlistVideoUrl(API_url,excelFolder,'19700101','20210420')
def getFavlistVideoUrl(API_url,excelFolder,beginTime,endTime):
    # 解析url
    url_parse=urlparse(API_url)
    # ParseResult(scheme='https', netloc='api.bilibili.com', path='/x/v3/fav/resource/list', params='',
    # query='media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp', fragment='')
    
    # 解析API_url中的query部分
    query=urlparse(API_url).query
    # 'media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'

    # 将query解析成字典
    query_dict=parse_qs(query)
    # {'media_id': ['1055169787'], 'pn': ['1'], 'ps': ['20'], 'order': ['mtime'], 'type': ['0'], 'tid': ['0'], 'platform': ['web'], 'jsonp': ['jsonp']}

    # 收藏夹页码
    pn=0
    # 判断是否有下一页
    has_more=True

    # 创建空数组，用于存放视频url
    np_videos=np.empty(shape=[0,8],dtype=np.str)
    # axis=0添加整行元素
    np_videos=np.append(np_videos,[["名称","视频分p数","视频时长","发布时间","收藏时间","视频稿件bvid","UP主","是否下载成功"]],axis=0)

    # 有效视频数量
    video_valid=0
    # 失效视频数量
    video_invalid=0

    # 遍历收藏夹的所有页
    # 如果has_more==True，则页码+1
    while has_more==True:
        # 页码+1
        pn+=1
        # 设置页码
        query_dict["pn"]=pn
        # 将dict类型参数转化为字符串
        query_str=urllib.parse.urlencode(query_dict,doseq=True)
        # 'media_id=1055169787&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
        
        # 修改query
        url_parse=url_parse._replace(query=query_str)
        # 拼合元素，更新url
        url_pn=url_parse.geturl()
        
        # 读取html文本信息
        r=getHTMLText(url_pn)
        # 将str转为json格式
        data = json.loads(r)
        # "title": "一千零一部", 收藏夹名称
        favlistName=data["data"]["info"]["title"]
        # "name": "木鱼水心", 收藏夹UP主
        favlistUpper=data["data"]["info"]["upper"]["name"]
        
        # 当前页面的视频信息
        data_videos=data["data"]["medias"]
        # 判断是否有下一页
        has_more=data["data"]["has_more"]
        # 遍历当前页面的视频信息
        for data_video in data_videos:
            # data_video=data_videos[0]
            # "title": "英法对决！哈克表情管理名场面！9.8分硬核神剧《是，首相》（06/S2E3&E4）", 视频名称
            # 规范化文件夹名称，去掉空格、/ \ : * ? " < > |
            title=data_video["title"]
            title=NormalFloderName(title)

            # "page": 1, 视频分P数
            page=data_video["page"]
            # "duration": 2396, 视频时长(秒)
            duration=data_video["duration"]
            if duration<3600:
                duration_str="%02d:%02d" % (duration // 60,duration % 60)
            # 时长可能会超过1小时
            else:
                duration_str="%02d:%02d:%02d" % (duration // 3600,duration %3600 // 60,duration % 60)
            
            # "ctime": 1610036663, 用户投稿时间
            # "pubtime": 1610036663, 稿件发布时间
            # "fav_time": 1610090951, 收藏时间
            pubtime=data_video["pubtime"]
            pubtime_str=getDateStr(pubtime)
            # 20210108

            fav_time=data_video["fav_time"]
            fav_time_str=getDateStr(fav_time)
            if fav_time_str>endTime:
                continue
            if fav_time_str<beginTime:
                break
            
            # "bvid": "BV1Bp4y1s7Th",视频稿件bvid
            bvid=data_video["bvid"]

            # "name": "木鱼水心",UP主名称
            upper=data_video["upper"]["name"]
            
            # 如果视频失效
            if title=='已失效视频':
                video_invalid+=1
            # 如果视频有效，就下载视频
            else:
                video_valid+=1
                np_videos=np.append(np_videos,[[title,page,duration_str,pubtime_str,fav_time_str,bvid,upper,'']],axis=0)
    
    print("视频数量：%d，有效视频数量：%d，失效视频数量：%d" % (video_invalid+video_valid,video_valid,video_invalid))

    # 存放视频url的excel文件
    excelFile=os.path.join(excelFolder,'收藏夹'+'_'+favlistUpper+'_'+favlistName+'_'+beginTime+'_'+endTime+'.xlsx')

    # 写入Excel文件
    data_excel = pd.DataFrame(np_videos)
    writer = pd.ExcelWriter(excelFile)
    data_excel.to_excel(writer, index=None, header=None) 
    writer.save()
    writer.close()
    # 返回excel文件位置
    return excelFile


# 投稿空间API，批量获得投稿视频的url
# API_url：API的url
# excelFolder：文件夹，用于存放包含视频url的excel表格文件
# API_url='https://api.bilibili.com/x/space/arc/search?mid=258150656&ps=30&tid=0&pn=1&order=pubdate&jsonp=jsonp'
# beginTime：视频最早发布时间，默认值是'19700101'
# endTime：视频最迟发布时间，默认值是当前日期8位字符串
# getContriVideoUrl(API_url,excelFolder,'19700101','20210420')
def getContriVideoUrl(API_url,excelFolder,beginTime,endTime):
    # 解析url
    url_parse=urlparse(API_url)
    # ParseResult(scheme='https', netloc='api.bilibili.com', path='/x/space/arc/search',
    # params='', query='mid=258150656&ps=30&tid=0&pn=1&order=pubdate&jsonp=jsonp', fragment='')

    # 解析API_url中的query部分
    query=urlparse(API_url).query
    # 'mid=258150656&ps=30&tid=0&pn=1&order=pubdate&jsonp=jsonp'

    # 将query解析成字典
    query_dict=parse_qs(query)
    # {'mid': ['258150656'], 'ps': ['30'], 'tid': ['0'], 'pn': ['1'], 'order': ['pubdate'], 'jsonp': ['jsonp']}

    # 投稿空间页码
    pn=0
    # 每页视频数量，默认值设置为30
    ps=30
    # 投稿空间视频总数量，默认值设置为1
    count=1

    # 创建空数组，用于存放视频url
    np_videos=np.empty(shape=[0,8],dtype=np.str)
    # axis=0添加整行元素
    np_videos=np.append(np_videos,[["名称","视频分p数","视频时长","发布时间","收藏时间","视频稿件bvid","UP主","是否下载成功"]],axis=0)

    # 有效视频数量
    video_valid=0
    # 失效视频数量
    video_invalid=0

    # 判断是否有下一页的方法：API记录的信息有页码、每页数量和总数量，
    # 当页码、每页数量大于等于总数量时，没有下一页
    while pn*ps<count:
        # 页码+1
        pn+=1
        # 设置页码
        query_dict["pn"]=pn
        # 将dict类型参数转化为字符串
        query_str=urllib.parse.urlencode(query_dict,doseq=True)
        # 'mid=258150656&ps=30&tid=0&pn=1&order=pubdate&jsonp=jsonp'
        
        # 修改query部分
        url_parse=url_parse._replace(query=query_str)
        # 拼合元素，更新url
        url_pn=url_parse.geturl()

        # 读取html文本信息
        r=getHTMLText(url_pn)
        # 将str转为json格式
        data = json.loads(r)
        # 当前页面的视频信息
        data_videos=data["data"]["list"]["vlist"]
        # 每页视频数量，默认值设置为30
        ps=data["data"]["page"]["ps"]
        # 投稿空间视频总数量
        count=data["data"]["page"]["count"]
        
        # 遍历当前页面的视频信息
        for data_video in data_videos:
            # "title": "【回形针PaperClip × 沃尔沃】汽车车身如何护你周全？", 视频名称
            # 规范化文件夹名称，去掉空格、/ \ : * ? " < > |
            title=data_video["title"]
            title=NormalFloderName(title)

            # "page": 1, 视频分P数
            # 投稿视频应该都是单集
            page=1
            # "length": "05:08", 视频时长(秒)
            length=data_video["length"]
            
            # "created": 1618578002, 稿件发布时间
            created=data_video["created"]
            created_str = getDateStr(created)

            if created_str>endTime:
                continue
            if created_str<beginTime:
                break

            # "bvid": "BV1Tf4y1s7pE",视频稿件bvid
            bvid=data_video["bvid"]

            # "author": "回形针PaperClip", UP主名称
            author=data_video["author"]
            
            # 如果视频失效
            if title=='已失效视频':
                video_invalid+=1
            # 如果视频有效，就下载视频
            else:
                video_valid+=1
                # 收藏时间为空
                np_videos=np.append(np_videos,[[title,page,length,created_str,'',bvid,author,'']],axis=0)
    
    print("视频数量：%d，有效视频数量：%d，失效视频数量：%d" % (video_invalid+video_valid,video_valid,video_invalid))
    
    excelFile=os.path.join(excelFolder,'投稿'+'_'+author+'_'+beginTime+'_'+endTime+'.xlsx')
    
    # 写入Excel文件
    data_excel = pd.DataFrame(np_videos)
    writer = pd.ExcelWriter(excelFile)
    data_excel.to_excel(writer, index=None, header=None) 
    writer.save()
    writer.close()
    # 返回excel文件位置
    return excelFile
