import os
import shutil
import logging

class CopyFile:
    '''
        目的：
        1.升级部署时，为了防止文件手动拷贝造成错误。
        2.提高工作效率
        
        思路：
        1.
        
        遇到问题：
        2020年4月15日17:51:35
        1. 限制遍历层级
    '''
    def __init__(self, src, dst, filter_folder, filter_file_suffix):
        # 确定新文件夹和老文件夹位置
        self.src = src
        self.dst = dst
        self.filter_folder = filter_folder
        self.filter_file_suffix = filter_file_suffix

    # 遍历出要操作的目录
    def search_dir(self, keyword):
        lists = os.listdir(self.src)  # 目录下的所有文件列变胖
        operating_dir = []  # 要操作的列表
        for lis in lists:  # 遍历出所有的目录
            if keyword in lis:  # 关键字在目录中
                operating_dir.append(lis)
                # logging.info(lis)
        return operating_dir  # 返回需要操作的列表

    # copy前台文件
    def copy_pre_file(self, keyword):
        folder_lists = self.search_dir(keyword)  # 获取操作目录列表
        # logging.info(folder_lists)
        for folder in folder_lists:  # 遍历出单个目录
            source_path = os.path.join(self.src, folder)  # 单个源文件目录完整地址
            target_path = os.path.join(self.dst, folder)  # 单个目标文件目录完整地址
            for i in os.listdir(source_path):
                source_path_file = os.path.join(source_path,i)
                logging.info(source_path_file)
            # logging.info(os.listdir(source_path))
            # logging.info(target_path)
                shutil.copy(source_path_file, target_path)
            # for root, dirs, files in os.walk(source_path):
            #     for file in files:
            #         src_file = os.path.join(root, file)
            #         logging.info(src_file)
            #         shutil.copy2(src_file, target_path)
            #         print(src_file)
    # copy后台文件
    def copy_bg_file(self):
        for file in all_file:
            suffix_list = file.split('.')
            for str in suffix_list:
                if str in self.filter_file_suffix:
                    # logging.info(file)
                    full_file_path = os.path.join(folder, file)
                    need_copy_list.append(full_file_path)
                    logging.info(full_file_path)
                    # print(full_file_path)
        return need_copy_list

# 筛选新文件夹内的以什么格式结尾的文件
# for i in lists:
#     houzhui = i.split('.')
#     if houzhui[1] in yes:
#         copy_path = os.path.join(new,i)
#         shutil.copy2(copy_path,old)
#         print(copy_path)
    # print(houzhui)
# 把新文件夹内文件复制到老文件夹

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format = '%(asctime)s - %(lineno)d - %(levelname)s - %(message)s')
    src_path = r'F:\python\copy_file\temp\src'  # 源文件地址（即将发布的）
    dst_path = r'F:\python\copy_file\temp\dst'  # 目标文件地址（线上正在运行的）
    folder_lists = ["网管后台", "文网前台"]  # 需要进行copy的文件夹
    file_suffix = ["pdf", "png"]  # 需要进行copy的文件后缀
    copy_file = CopyFile(src_path, dst_path, folder_lists, file_suffix)
    # copy_file.get_file('后台')
    # copy_file.copy_pre_file('前台')
    copy_file.copy_pre_file('前台')