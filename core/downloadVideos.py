# 为了调用os.system(command)
import os
# 操作excel
import numpy as np
import pandas as pd

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


# 批量下载视频
# excelFile：存放视频url的excel表格文件
# downloadFolder：视频下载到哪个文件夹
# videoType：视频类型，0：收藏夹视频，1：投稿视频
# beginTime：视频最早发布时间，默认值是'19700101'
def BatchDownloadVideos(excelFile,downloadFolder,videoType,beginTime='19700101'):
    # os.path.split(excelFile)
    # ('D:\\00Gerc\\XueXi20200104\\00Desktop\\我的笔记20200311\\00葛荣存\\个人项目笔记\\20210418批量下载B站视频
    # \\Github项目\\result\\00视频信息Excel文件', '投稿_回形针PaperClip_20210420.xlsx')
    
    # 在downloadFolder下创建新文件夹，用于存放本次下载的所有视频
    downloadFolder=os.path.join(downloadFolder,os.path.split(excelFile)[1][:-5])
    # 投稿_回形针PaperClip_20210420
    if not os.path.exists(downloadFolder):
        os.mkdir(downloadFolder)

    # 读取excel表格
    df=pd.read_excel(excelFile, sheet_name=0, header=None, index_col=None,na_values=['NA'],dtype='str')
    records=df.to_numpy()

    # 视频序号，记录下载到第几个视频，方便把握下载进度
    orderVideo=0

    # 遍历每一行
    # 第一行是列名
    for record in records[1:]:
        # record=records[1]
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
        # 收藏时间
        mtime=record[4]
        # 视频bvid
        bvid=record[5]
        # UP主姓名
        upper=record[6]
        
        # 确定视频时间，跟beginTime比较
        # videoType，0：收藏夹视频，1：投稿视频
        if videoType==0:
            timeVideo=mtime
        else:
            timeVideo=pubtime
        if timeVideo<beginTime:
            break
        
        # 输出信息，方便了解视频信息
        # len(records)-1，第一行是列名
        print("序号：%d//%d，名称：%s，时长：%s" % (orderVideo,len(records)-1,title,duration))
        # 拼合出视频url
        video_url='https://www.bilibili.com/video/'+bvid
        # 文件夹位置，为视频创建一个文件夹
        folderName=str(pubtime)+'_'+upper+'_'+title+'_'+'B站'+'_'+bvid
        folder=os.path.join(downloadFolder,folderName)
        # 下载视频，并判断是否下载成功
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