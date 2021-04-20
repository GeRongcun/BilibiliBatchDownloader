# 操作文件目录
import os

# 项目文件夹位置
projectFolder=r'D:/00Gerc/XueXi20200104/00Desktop/我的笔记20200311/00葛荣存/个人项目笔记/20210418批量下载B站视频/Github项目'
# 代码文件夹位置
coreFolder=os.path.join(projectFolder,'core')
os.chdir(coreFolder) # 打开文件目录，相当于cd

# 导入自定义模块
import getVideoUrl
import downloadVideos

# 视频下载到哪个文件夹
downloadFolder=os.path.join(projectFolder,'result')
# excelFolder：文件夹，用于存放包含视频url的excel表格文件
excelFolder=os.path.join(downloadFolder,'00视频信息Excel文件')

# 根据收藏夹url，批量下载视频
def downloadFavlistVideos(fav_url,beginTime='19700101'):
    # 根据收藏夹url，获得API_url
    fav_API_url=getVideoUrl.getFavlistAPI_url(fav_url)
    # 收藏夹视频API，批量获得收藏夹视频的url
    excelFile=getVideoUrl.getFavlistVideoUrl(fav_API_url,excelFolder)
    # 批量下载视频
    downloadVideos.BatchDownloadVideos(excelFile,downloadFolder,0,beginTime)

# 根据投稿空间url，批量下载视频
def downloadContributionVideos(contri_url,beginTime='19700101'):
    # UP主投稿空间url，获得API_url
    contri_API_url=getVideoUrl.getContriAPI_url(contri_url)
    # 投稿空间API，批量获得投稿视频的url
    excelFile=getVideoUrl.getContriVideoUrl(contri_API_url,excelFolder)
    # 批量下载视频
    downloadVideos.BatchDownloadVideos(excelFile,downloadFolder,1,beginTime)

# main函数
def main():
    # 收藏夹url，favlist
    # fav_url='https://space.bilibili.com/927587/favlist?fid=1055169787&ftype=create'
    fav_url='https://space.bilibili.com/91724487/favlist?fid=204884287&ftype=create'
    # UP主投稿空间url，contribution
    contri_url='https://space.bilibili.com/258150656/video?tid=0&page=2&keyword=&order=pubdate'

    downloadFavlistVideos(fav_url,'20210329')
    downloadContributionVideos(contri_url,'20200929')
    downloadContributionVideos(contri_url,'20210415')
if __name__ == '__main__':
    main()