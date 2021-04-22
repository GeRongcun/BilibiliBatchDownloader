# 操作文件目录
import os
import shutil

# 有些视频是单集视频，有些视频是合集视频
# 无论是单集视频还是合集视频，我们都为其创建了文件夹存放
# 对于单集视频，将视频从文件夹中移出来，并重命名
# 对于合集视频，还放在文件夹中，并重命名
downloadFolder_videoList=r'D:\00Gerc\XueXi20200104\00Desktop\我的笔记20200311\00葛荣存\个人项目笔记\20210418批量下载B站视频\批量下载B站视频\result\投稿_回形针PaperClip_20201224_20210422'
def RenameFiles(downloadFolder_videoList):
    # 打开文件目录，相当于cd
    os.chdir(downloadFolder_videoList)
    # 列出所有文件夹，相当于dir
    folderList=os.listdir()
    # 遍历全部文件夹
    for folder in folderList:
        # folder=folderList[-5]
        os.chdir(downloadFolder_videoList)
        if not os.path.isdir(os.path.join(downloadFolder_videoList,folder)):
            continue
        os.chdir(os.path.join(downloadFolder_videoList,folder))
        # 列出所有文件，相当于dir
        fileList=os.listdir()
        # 删除弹幕文件
        for f in fileList:
            # f=fileList[1]
            # 如果是xml文件，删除
            if f[-4:]=='.xml':
                os.remove(f)
        # 如果文件夹中的视频文件数量大于1，则说明是合集，不进行操作
        if len(fileList)>1:
            continue
        # 遍历文件
        for f in fileList:
            if f[-4:]=='.flv':
                shutil.move(f,os.path.join(downloadFolder_videoList,folder+'.flv'))
        # 删除空目录
        # 删除空目录老是报错，可以重命名文件夹，手动删除
        os.chdir(downloadFolder_videoList)
        os.rename(folder,'00删除_'+folder)


