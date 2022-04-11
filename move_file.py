import os
import time
from shutil import copyfile


# 读取txt文件  并保存检索到的docx文件信息
def read_txt(txt_path):
    content = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f.readlines():
            data = line.replace("\n", "")
            if ".docx" in data:
                print(data)
                content.append(data)
    return content


# 将检索出的docx文件单独放入一个新的文件夹
def move_docx(path_list):
    for docx_name in path_list:
        docx_path = ".\\saver\\" + docx_name
        to_path = ".\\target_files\\" + docx_name
        # 复制并粘贴
        copyfile(docx_path, to_path)


if __name__ == '__main__':
    t = time.time()
    txt_path = "pathAndName.txt"
    # 读取检索txt文件
    from_path_list = read_txt(txt_path)
    # 并进行文件复制粘贴
    move_docx(from_path_list)
    print(time.time() - t)



