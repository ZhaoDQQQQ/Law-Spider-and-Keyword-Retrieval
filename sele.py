from selenium import webdriver
import time
from urllib import request
from bs4 import BeautifulSoup
import json
from selenium.webdriver.common.by import By


# 生产者  提供文件下载地址URL
class Producer:
    # 初始化
    def __init__(self):
        # URL地址前半部分   选择页数
        self.start_url = "https://flk.npc.gov.cn/api/?page="
        # URL地址后半部分   选择页数
        self.end_url = "&type=dfxfg&searchType=title%3Baccurate&sortTr=f_bbrq_s%3Bdesc&gbrqStart=&gbrqEnd=&" \
                       "sxrqStart=&sxrqEnd=&sort=true&size=10"
        # 请求URL得到的信息  一页（10个）的相关法律文件的阅览地址
        self.data = []
        # 当前页  第几个  num
        self.num = 0

    def set_page(self, i):
        # 生成请求URL，i代表页码
        URL = self.start_url + str(i) + self.end_url
        # 进行请求
        req = request.Request(URL, headers={'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'})
        # 获取数据并解码
        page = request.urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        page.close()

        # 获取一页（10个）的相关法律文件的信息
        info = soup.find("p").contents[0].text
        info = json.loads(info)
        self.data = info["result"]["data"]
        self.num = 0
        # 暂停一会儿  反爬
        time.sleep(0.2)

    # 获取下一个法律文件的阅览地址
    def next(self):
        res = self.data[self.num]
        self.num += 1
        return res


if __name__ == '__main__':
    producer = Producer()
    # 浏览器模拟爬取   可以采用无页面浏览器  这里采用的chrome浏览器
    driver = webdriver.Chrome()
    driver.maximize_window()
    # 遍历循环  0-1799页
    for i in range(0, 1799):
        # 获取第i页的信息
        producer.set_page(i)
        print(i)
        # 依次下载10个法律文件
        # 因为法律文件的阅览模式是类似PDF的形式，无法直接进行关键字的检索  所以采用先下载后检索的方式  下载后为docx格式
        for j in range(10):
            # 获取下一个地址
            x = producer.next()
            driver.get(x["url"])
            time.sleep(0.2)
            # 找到下载按钮
            x = driver.find_element(By.ID, "downLoadFile")
            #  地方性法规部分无法下载，无下载链接
            try:
                # 模拟点击  进行下载
                x.click()
            except:
                # 无法下载  则进行输出  概率很小  大概存在1%的文件无法下载
                print((i, j), "not find")



