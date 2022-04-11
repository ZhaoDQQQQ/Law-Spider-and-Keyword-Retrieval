from win32com import client as wc
import os
import time


# 获取文件夹中特定后缀的文件
# 因为下载下来的文件存在doc docx  pdf多种格式
def get_specific_suffix_file(dir_path, store_list=[], suffix_name=".doc"):
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if os.path.splitext(file)[1] == suffix_name:
                store_list.append(os.path.join(root, file))
    return store_list


# 将doc格式的文件转换为docx格式的文件
def doc_to_docx(doc_files):
    word = wc.Dispatch('Word.Application')
    for i in range(len(doc_files)):
        doc_file_path = doc_files[i]
        # [1:]  是因为相对路径字符串第一个字符为  “.”
        # 下面word.Documents.Open需要绝对路径
        doc_file_path = "E:\\PycharmProjects\\DownloadAndSearch" + doc_file_path[1:]
        print(i, doc_file_path)
        doc = word.Documents.Open(doc_file_path)
        doc_name = doc_file_path.split("\\")[4]
        doc_name = doc_name.split(".")[0]
        # 转换后的docx格式文件  被保存到的路径
        target_docx_file_path = "E:\\PycharmProjects\\DownloadAndSearch\\saver3\\" + doc_name + ".docx"
        # print(target_docx_file_path)
        # 进行保存
        doc.SaveAs(target_docx_file_path, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
        doc.Close()
    word.Quit()


if __name__ == '__main__':
    # 因为python操作doc文件不方便  该部分代码用于将doc文件转换为docx文件  然后再进行相关检索操作
    t = time.time()
    start_path = ".\\saver"
    # 获取后缀为doc的文件
    doc_files = get_specific_suffix_file(start_path, [], ".doc")
    print(len(doc_files))
    # 将doc文件转换为docx格式文件
    doc_to_docx(doc_files)
    print(time.time() - t)
