# 为了调用os.system(command)
import os
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

# 下载视频
# url：视频url
# url='https://www.bilibili.com/video/BV1wt411j7WF'
# downloadFolder：视频下载到哪个文件夹
# 菜鸟历险记分集
def downloadVideo(url,downloadFolder):
    # --playlist的作用：如果该视频是合集视频，则下载合集，如果该视频不是合集视频，则直接下载
    # -o：指定视频下载到哪个文件夹
    command='you-get --playlist -o '+downloadFolder+' '+url
    # 执行命令行命令
    return os.system(command)
    # 返回0，下载成功；返回1，下载失败

# 获得html文本信息
def getHTMLText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()  #如果状态不是200，引发异常
        r.encoding='utf-8' #无论原来用什么编码，都改成utf-8
        return r.text 
    except:
        return ""

# 通过收藏夹url获得fav_API_url
# fav_url：收藏夹网址
# fav_url='https://space.bilibili.com/91724487/favlist?fid=204884287&ftype=create'
def getFavlistAPI_url(fav_url):
    # 解析url的query部分
    fav_url_query=urlparse(fav_url).query
    # 将query解析成字典
    fav_url_dict=parse_qs(fav_url_query)
    # {'fid': ['204884287'], 'ftype': ['create']}
    # 获得收藏夹网址中的fid
    fav_url_query_fid=fav_url_dict["fid"]
    # ['204884287']

    # fav_API_url模板
    fav_API_url='https://api.bilibili.com/x/v3/fav/resource/list?media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    # 解析fav_API_url的query
    fav_API_url_query=urlparse(fav_API_url).query
    # 'media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    # fav_API_url的query解析成字典
    fav_API_url_dict=parse_qs(fav_API_url_query)
    # {'media_id': ['1055169787'], 'pn': ['1'], 'ps': ['20'], 'order': ['mtime'], 
    # 'type': ['0'], 'tid': ['0'], 'platform': ['web'], 'jsonp': ['jsonp']}
    
    # 将fav_API_url中的media_id修改成fid即可
    fav_API_url_dict["media_id"]=fav_url_query_fid
    # 将页码设置为1，便于从第1页往后遍历收藏夹的所有页
    fav_API_url_dict["pn"]=1

    # 将dict类型参数转化为query_string格式
    fav_API_url_query=urllib.parse.urlencode(fav_API_url_dict,doseq=True)
    # 'media_id=204884287&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    fav_API_url='https://api.bilibili.com/x/v3/fav/resource/list?'+fav_API_url_query

    # 'https://api.bilibili.com/x/v3/fav/resource/list?media_id=204884287&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    return fav_API_url

# 通过UP主投稿视频url获得upload_API_url
# upload_url：UP主投稿视频url
# upload_url='https://space.bilibili.com/258150656/video?tid=0&page=2&keyword=&order=pubdate'
def getUplistAPI_url(upload_url):
    # 解析url的pash部分
    upload_url_path=urlparse(upload_url).path
    # '/258150656/video'

    # 获得mid
    mid=upload_url_path.split('/')[1]
    # '258150656'

    # 解析url的query部分
    upload_url_query=urlparse(upload_url).query
    # 将query解析成字典
    upload_url_dict=parse_qs(upload_url_query)
    # {'tid': ['0'], 'page': ['2'], 'order': ['pubdate']}

    # upload_API_url模板
    upload_API_url='https://api.bilibili.com/x/space/arc/search?mid=258150656&ps=30&tid=0&pn=2&keyword=&order=pubdate&jsonp=jsonp'
    
    # 解析upload_API_url的query
    upload_API_url_query=urlparse(upload_API_url).query
    # 'mid=258150656&ps=30&tid=0&pn=2&keyword=&order=pubdate&jsonp=jsonp'
    # upload_API_url的query解析成字典
    upload_API_url_dict=parse_qs(upload_API_url_query)
    # {'mid': ['258150656'], 'ps': ['30'], 'tid': ['0'], 'pn': ['2'], 'order': ['pubdate'], 'jsonp': ['jsonp']}
    
    # 将API_url中的media_id修改成fid即可
    upload_API_url_dict["mid"]=mid
    # 将页码设置为1，便于从第1页往后遍历收藏夹的所有页
    upload_API_url_dict["pn"]=1

    # 将dict类型参数转化为query_string格式
    upload_API_url_query=urllib.parse.urlencode(upload_API_url_dict,doseq=True)
    # 'media_id=204884287&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
    upload_API_url='https://api.bilibili.com/x/space/arc/search?'+upload_API_url_query

    # 'https://api.bilibili.com/x/space/arc/search?mid=258150656&ps=30&tid=0&pn=1&order=pubdate&jsonp=jsonp'
    return upload_API_url


# 收藏夹视频API，批量获得收藏夹视频的url
# API_url：API的url
# excelFile：存放视频url的excel表格文件
# fav_url='https://space.bilibili.com/927587/favlist?fid=1055169787&ftype=create'
# API_url='https://api.bilibili.com/x/v3/fav/resource/list?media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
def getFavlistVideoUrl(API_url,excelFile):
    # 解析url
    url_parse=urlparse(API_url)
    # ParseResult(scheme='https', netloc='api.bilibili.com', path='/x/v3/fav/resource/list', params='',
    #  query='media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp', fragment='')
    
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
    np_videos=np.empty(shape=[0,7],dtype=np.str)
    # axis=0添加整行元素
    np_videos=np.append(np_videos,[["名称","视频分p数","视频时长","发布时间","视频稿件bvid","UP主","是否下载成功"]],axis=0)

    # 有效视频数量
    video_valid=0
    # 失效视频数量
    video_invalid=0

    # 如果has_more==True，则页码+1，遍历一遍
    while has_more==True:
        # 页码+1
        pn+=1
        # 设置页码
        query_dict["pn"]=pn
        # 将dict类型参数转化为字符串
        query_str=urllib.parse.urlencode(query_dict,doseq=True)
        # 'media_id=1055169787&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
        
        # 修改query部分
        url_parse=url_parse._replace(query=query_str)
        # 拼合元素，更新url
        url_pn=url_parse.geturl()
        
        # 读取html文本信息
        r=getHTMLText(url_pn)
        # 将str转为json格式
        data = json.loads(r)
        # 当前页面的视频信息
        data_videos=data["data"]["medias"]
        # 判断是否有下一页
        has_more=data["data"]["has_more"]
        # 遍历当前页面的视频信息
        for data_video in data_videos:
            # "title": "英法对决！哈克表情管理名场面！9.8分硬核神剧《是，首相》（06/S2E3&E4）", 视频名称
            # 去掉标题中的空格，不然后面创建文件夹会报错
            title=data_video["title"].replace(" ", "")

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
            pubtime_Array = time.localtime(pubtime)
            # time.struct_time(tm_year=2021, tm_mon=1, tm_mday=8, tm_hour=0, 
            # tm_min=24, tm_sec=23, tm_wday=4, tm_yday=8, tm_isdst=0)
            pubtime_str = "%04d%02d%02d" % (pubtime_Array.tm_year,pubtime_Array.tm_mon,pubtime_Array.tm_mday)

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
                np_videos=np.append(np_videos,[[title,page,duration_str,pubtime_str,bvid,upper,'']],axis=0)
    
    print("视频数量：%d，有效视频数量：%d，失效视频数量：%d" % (video_invalid+video_valid,video_valid,video_invalid))
    # 写入Excel文件
    data_excel = pd.DataFrame(np_videos)
    writer = pd.ExcelWriter(excelFile)
    data_excel.to_excel(writer, index=None, header=None) 
    writer.save()
    writer.close()


# UP主投稿视频API，批量获得UP主投稿视频的url
# API_url：API的url
# excelFile：存放视频url的excel表格文件
# fav_url='https://space.bilibili.com/927587/favlist?fid=1055169787&ftype=create'
# API_url='https://api.bilibili.com/x/v3/fav/resource/list?media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
def getFavlistVideoUrl(API_url,excelFile):
    # 解析url
    url_parse=urlparse(API_url)
    # ParseResult(scheme='https', netloc='api.bilibili.com', path='/x/v3/fav/resource/list', params='',
    #  query='media_id=1055169787&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp', fragment='')
    
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
    np_videos=np.empty(shape=[0,7],dtype=np.str)
    # axis=0添加整行元素
    np_videos=np.append(np_videos,[["名称","视频分p数","视频时长","发布时间","视频稿件bvid","UP主","是否下载成功"]],axis=0)

    # 有效视频数量
    video_valid=0
    # 失效视频数量
    video_invalid=0

    # 如果has_more==True，则页码+1，遍历一遍
    while has_more==True:
        # 页码+1
        pn+=1
        # 设置页码
        query_dict["pn"]=pn
        # 将dict类型参数转化为字符串
        query_str=urllib.parse.urlencode(query_dict,doseq=True)
        # 'media_id=1055169787&pn=1&ps=20&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp'
        
        # 修改query部分
        url_parse=url_parse._replace(query=query_str)
        # 拼合元素，更新url
        url_pn=url_parse.geturl()
        
        # 读取html文本信息
        r=getHTMLText(url_pn)
        # 将str转为json格式
        data = json.loads(r)
        # 当前页面的视频信息
        data_videos=data["data"]["medias"]
        # 判断是否有下一页
        has_more=data["data"]["has_more"]
        # 遍历当前页面的视频信息
        for data_video in data_videos:
            # "title": "英法对决！哈克表情管理名场面！9.8分硬核神剧《是，首相》（06/S2E3&E4）", 视频名称
            # 去掉标题中的空格，不然后面创建文件夹会报错
            title=data_video["title"].replace(" ", "")

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
            pubtime_Array = time.localtime(pubtime)
            # time.struct_time(tm_year=2021, tm_mon=1, tm_mday=8, tm_hour=0, 
            # tm_min=24, tm_sec=23, tm_wday=4, tm_yday=8, tm_isdst=0)
            pubtime_str = "%04d%02d%02d" % (pubtime_Array.tm_year,pubtime_Array.tm_mon,pubtime_Array.tm_mday)

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
                np_videos=np.append(np_videos,[[title,page,duration_str,pubtime_str,bvid,upper,'']],axis=0)
    
    print("视频数量：%d，有效视频数量：%d，失效视频数量：%d" % (video_invalid+video_valid,video_valid,video_invalid))
    # 写入Excel文件
    data_excel = pd.DataFrame(np_videos)
    writer = pd.ExcelWriter(excelFile)
    data_excel.to_excel(writer, index=None, header=None) 
    writer.save()
    writer.close()


# 批量下载视频
# excelFile：存放视频url的excel表格文件
# downloadFolder：视频下载到哪个文件夹
def BatchDownloadVideos(excelFile,downloadFolder):
    # 读取excel表格
    df=pd.read_excel(excelFile, sheet_name=0, header=None, index_col=None,na_values=['NA'],dtype='str')
    records=df.to_numpy()

    # 视频序号，记录下载到第几个视频，方便把握下载进度
    orderVideo=0

    # 遍历每一行
    for record in records[1:]:
        # 视频序号+1
        orderVideo+=1
        # 视频名称
        title=record[0]
        # 视频分p数
        page=record[1]
        # 视频时长
        duration=record[2]
        # 视频发布时间
        pubtime=record[3]
        # 视频bvid
        bvid=record[4]
        # UP主姓名
        upper=record[5]
        # 输出信息，方便了解视频信息
        print("序号：%d//%d，名称：%s，时长：%s" % (orderVideo,len(records),title,duration))
        # 拼合出视频url
        video_url='https://www.bilibili.com/video/'+bvid
        # 文件夹位置，为视频创建一个文件夹
        folderName=str(pubtime)+'_'+upper+'_'+title+'_'+'B站'+'_'+bvid
        folder=os.path.join(downloadFolder,folderName)
        # 下载视频
        isSuccess=downloadVideo(video_url,folder)
        if isSuccess==0:
            record[6]='0'
        else:
            record[6]=str(isSuccess)
    # 写入Excel文件
    data_excel = pd.DataFrame(records)
    writer = pd.ExcelWriter(excelFile)
    data_excel.to_excel(writer, index=None, header=None)
    writer.save()
    writer.close()


# 项目文件夹位置
projectFolder=r'D:\00Gerc\XueXi20200104\00Desktop\我的笔记20200311\00葛荣存\个人项目笔记\20210418批量下载B站视频'
# 视频下载到哪个文件夹
downloadFolder=os.path.join(projectFolder,'Result')
# excelFile：存放视频url的excel表格文件
excelFile=os.path.join(projectFolder,'视频列表.xlsx')
# 收藏夹url
# fav_url='https://space.bilibili.com/927587/favlist?fid=1055169787&ftype=create'
fav_url='https://space.bilibili.com/91724487/favlist?fid=204884287&ftype=create'
# UP主投稿url
upload_url='https://space.bilibili.com/258150656/video?tid=0&page=2&keyword=&order=pubdate'

# main函数
def main():
    # 根据收藏夹url，获得API_url
    fav_API_url=getFavlistAPI_url(fav_url)
    # 收藏夹视频API，批量获得收藏夹视频的url
    getFavlistVideoUrl(fav_API_url,excelFile)
    # 批量下载视频
    BatchDownloadVideos(excelFile,downloadFolder)

    upload_API_url=getUplistAPI_url(upload_url)
upload_API_url
if __name__ == '__main__':
    main()

