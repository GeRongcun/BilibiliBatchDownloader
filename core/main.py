# 操作文件目录
import os

# 项目文件夹位置
projectFolder=r'D:\00Gerc\XueXi20200104\00Desktop\我的笔记20200311\00葛荣存\个人项目笔记\20210418批量下载B站视频\批量下载B站视频'
# 代码文件夹位置
coreFolder=os.path.join(projectFolder,'core')
os.chdir(coreFolder) # 打开文件目录，相当于cd

# 导入自定义模块
import getVideoUrl
import downloadVideos
import renameFiles

# 存放所有收藏夹或投稿空间的视频
resultFolder=os.path.join(projectFolder,'result')
# excelFolder：文件夹，用于存放包含视频url的excel表格文件
excelFolder=os.path.join(resultFolder,'00视频信息Excel文件')

# 根据收藏夹url，批量下载视频
def downloadFavlistVideos(fav_url,beginTime='19700101',endTime=getVideoUrl.getDateStr()):
    # beginTime='19700101'
    # endTime='20210421'
    # 根据收藏夹url，获得API_url
    fav_API_url=getVideoUrl.getFavlistAPI_url(fav_url)
    # 收藏夹视频API，批量获得收藏夹视频的url
    excelFile=getVideoUrl.getFavlistVideoUrl(fav_API_url,excelFolder,beginTime,endTime)
    # 批量下载视频
    # 存放单个收藏夹或投稿空间的视频
    downloadFolder_videoList=downloadVideos.BatchDownloadVideos(excelFile,resultFolder,0)
    return downloadFolder_videoList

# 根据投稿空间url，批量下载视频
def downloadContributionVideos(contri_url,beginTime='19700101',endTime=getVideoUrl.getDateStr()):
    # beginTime='19700101'
    # endTime='20210421'
    # UP主投稿空间url，获得API_url
    contri_API_url=getVideoUrl.getContriAPI_url(contri_url)
    # 投稿空间API，批量获得投稿视频的url
    excelFile=getVideoUrl.getContriVideoUrl(contri_API_url,excelFolder,beginTime,endTime)
    # 存放单个收藏夹或投稿空间的视频
    downloadFolder_videoList=downloadVideos.BatchDownloadVideos(excelFile,resultFolder,1)
    return downloadFolder_videoList

# main函数
def main():
    # 回形针PaperClip投稿
    # contri_url='https://space.bilibili.com/258150656/video?tid=0&page=2&keyword=&order=pubdate'
    # downloadFolder_videoList=downloadContributionVideos(contri_url,'20201224','20210422')
    # renameFiles.RenameFiles(downloadFolder_videoList)
    
    # 划水小能手的收藏夹-学习
    # fav_url='https://space.bilibili.com/91724487/favlist?fid=204884287&ftype=create'
    # downloadFolder_videoList=downloadFavlistVideos(fav_url,'19700101','20210421')
    # renameFiles.RenameFiles(downloadFolder_videoList)

    # 划水小能手的收藏夹-驾驶
    # fav_url='https://space.bilibili.com/91724487/favlist?fid=1204908287&ftype=create'
    # downloadFolder_videoList=downloadFavlistVideos(fav_url,'19700101','20210422')
    # renameFiles.RenameFiles(downloadFolder_videoList)
if __name__ == '__main__':
    main()