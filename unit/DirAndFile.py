# encoding=utf-8
from config.Var import *
from logs.logger import Logger


def createDir(path, dirName):
    # os.path.join(x,y)是拼接路径用的
    dirPath = os.path.join(path, dirName)
    isExists = os.path.exists(dirPath)
    if not isExists:
        try:
            os.makedirs(dirPath)
        except Exception as e:
            print(e)
        return dirPath
    else:
        return dirPath
        pass

# a = createDir(project_path + "//ScreenPictures//CapturePictures", time.strftime("%Y-%m-%d"))
# print(a)

