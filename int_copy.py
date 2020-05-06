import os
import shutil
import time
import hashlib
import logging

# MD5值
def getMD5(path):
    f = open(path, 'rb')
    d5 = hashlib.md5()  # 生成一个hash的对象
    with open(path, 'rb') as f:
        while True:
            content = f.read(40960)
            if not content:
                break
            d5.update(content)  # 每次读取一部分，然后添加到hash对象里
    # print('MD5 : %s' % d5.hexdigest())
    return d5.hexdigest()  # 打印16进制的hash值


# 装饰器，计时用的
def timer(func):  # 高阶函数：以函数作为参数
    def deco(*args, **kwargs):  # 嵌套函数，在函数内部以 def 声明一个函数,接受 被装饰函数的所有参数
        time1 = time.time()
        func(*args, **kwargs)
        time2 = time.time()
        print('Elapsed %ss\n' % round(time2 - time1, 2))

    return deco  # 注意，返回的函数没有加括号！所以返回的是一个内存地址，而不是函数的返回值


@timer
def compare(baseFolder, targetFolder, content_compare='y'):
    '''
    baseFolder:   基础文件夹，将基础文件夹中的文件按照相应的目录结构同步到目标文件夹中。
    targetFolder: 目标文件夹
    content_compare: 是否比对两个文件的内容，默认比对，防止文件内容有更改。参数值如果不是'y',则不比对内容，只判断目标文件夹是否有同名文件，有就跳过，没有就复制过去。
    '''
    n = 0
    for path, subpath, files in os.walk(baseFolder):
        logging.info(path)
        logging.info(subpath)
        logging.info(files)
        for file in files:
            # 获取文件的绝对路径
            absPath = os.path.join(path, file)
            # 文件的后半截路径,即文件的相对路径
            file_path = absPath.replace(baseFolder, '')
            # 去掉路径前面的\
            if file_path[:1] == '\\':
                file_path = file_path[1:]

            # 替换目录末尾的\
            if targetFolder[:1] == '\\':
                targetFolder = targetFolder[1:]

            # 判断目标文件夹是否有相应的文件
            filePath = os.path.join(targetFolder, file_path)

            # 创建文件夹路径
            fileFolder = os.path.dirname(filePath)

            # 如果目标文件夹不存在此文件
            if not os.path.exists(filePath):
                os.makedirs(fileFolder, exist_ok=True)
                # 复制文件
                shutil.copy(absPath, fileFolder)
                print(f'\n     {absPath}   -------------->   {filePath}')
            else:  # 如果目标文件夹已经存在某文件
                # 如果要对比两个文件的内容
                if content_compare == 'y':
                    # 先对比两个文件的修改时间（谁的时间越大，代表谁的内容越新）
                    baseTime = os.stat(absPath).st_mtime
                    targetTime = os.stat(filePath).st_mtime
                    if baseTime - targetTime > 0:
                        # 比了时间，再比一下MD5。如果MD5也不同，就将这个时间最新的文件复制过去
                        baseMD5 = getMD5(absPath)
                        targetMD5 = getMD5(filePath)
                        if baseMD5 != targetMD5:
                            os.unlink(filePath)
                            shutil.copy(absPath, fileFolder)
                            print(f'\n     {absPath}   -------------->   {filePath}')
                        else:
                            # MD5相同，而目标文件夹中的时间又小，就将修改时间改大，防止下次运行此脚本时再对比一遍MD5，浪费时间
                            # 修改文件的访问和修改时间，改成当前系统时间
                            os.utime(filePath)
            n += 1
            print("\r%s:  Has scanned %s files. " % (baseFolder, n), end='')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(lineno)d - %(levelname)s - %(message)s')
    print('----------将源文件复制到已经部署的文件夹里----------')
    print('---------- 源文件-->>部署的文件 ----------\n')
    base = r'F:\python\copy_file\temp\src'
    target = r'F:\python\copy_file\temp\dst'
    print(r'源文件目录:F:\python\copy_file\temp\src')
    print(r'发布文件目录:F:\python\copy_file\temp\dst')
    # 当有相同文件时，是否对比文件内容，把最新的同步过去，适用于经常变动的文件，如脚本，文档
    content_compare = input('是否进行文件对比? y/n: ').lower()
    if base == '':
        compare(r'D:\备份', r'G:\备份')
        compare(r'D:\software', r'G:\software')
        compare(r'E:\文档', r'G:\document')
    else:
        compare(base, target, content_compare)