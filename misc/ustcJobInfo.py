__author__ = 'WCQ'
# -*- coding: utf-8 -*-

import urllib2
import urllib
import re
import MySQLdb
import thread
import time

#----------- 加载招聘信息 -----------
class Spider_Model:
    def __init__(self):
        self.page = 1
        self.enable = False
        self.endPage = 2

    # 获取网址的HTML 并编码
    def GetHTML(self, myUrl):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        req = urllib2.Request(myUrl, headers=headers)
        myResponse = urllib2.urlopen(req)
        myPage = myResponse.read()
        # encode的作用是将unicode编码转换成其他编码的字符串
        # decode的作用是将其他编码的字符串转换成unicode编码
        unicodePage = myPage.decode("GBK")
        utfcodePage = unicodePage.encode("utf-8")
        return unicodePage


    # 将招聘信息抠出来，添加到列表中并且返回列表
    def GetPage(self, page):
        myUrl = "http://www.job.ustc.edu.cn/list.php?trans=7&page=" + str(page) + "&MenuID=002002"
        unicodePage = self.GetHTML(myUrl)
        # 找出所有class="content"的div标记
        # re.S是任意匹配模式，也就是.可以匹配换行符
        jobList = re.findall('<div class="Joplistone">(.*?)</div>', unicodePage, re.S)
        jobItems = re.findall('<li><a href="(.*?)" style="color:#">(.*?)</a><span class="zhiwei">(.*?)</span><span class="zhuanye">(.*?)</span></li>', jobList[0], re.S)
        jobs = []
        for job in jobItems:
            # job 中第一个元素是招聘链接
            # job 中第二个元素是招聘公司
            # job 中第三个元素是职位
            # job 中第四个元素是发布日期
            jobs.append([job[1], "http://www.job.ustc.edu.cn/" + job[0], job[2], job[3]])
        return jobs

    # 获得招聘细节
    def getJobDetail(self, joburl):
        jobHtml = self.GetHTML(joburl)
        jobDetail = re.findall('<div class="textone">(.*?)</div>', jobHtml, re.S)
        #print jobDetail
        return jobDetail

    # 获得完整的招聘信息
    def getJobDetailList(self, jobs):
        jobDetailList = []
        for job in jobs:
            jobDetailList.append([job[0], job[1], job[2], job[3], self.getJobDetail(job[1])])
        return jobDetailList

    # 先展示一下
    def showJob(self, page):
        jobs = self.GetPage(page)
        jobDetailList = self.getJobDetailList(jobs)
        for jobDetail in jobDetailList:
            for iterm in jobDetail:
                print iterm

    # 创建表
    def creatTable(self):
        # 打开数据库连接
        db = MySQLdb.connect("localhost", "root", "6632023", "test")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        # 如果数据表已经存在使用 execute() 方法删除表。
        cursor.execute("DROP TABLE IF EXISTS jobs")
        # 创建数据表SQL语句
        sql = """CREATE TABLE jobs (
                    company  CHAR(255) NOT NULL,
                    link_address  CHAR(255),
                    occupation CHAR(255),
                    data char(255),
                    detail TEXT )"""
        cursor.execute(sql)
        db.commit()
        db.close()

    # 写入到数据库
    def writeTable(self, page):
        # 打开数据库连接
        db = MySQLdb.connect("localhost", "root", "6632023", "test")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        jobs = self.GetPage(page)
        jobDetailList = self.getJobDetailList(jobs)
        for jobDetail in jobDetailList:
            # 使用execute方法执行SQL语句
            cursor.execute("insert into jobs values(" + jobDetail[0]+","+jobDetail[1]+","+ jobDetail[2]+","+ jobDetail[3]+","+ str(jobDetail[4]).encode("utf-8") + ")")
            # 要提交
            db.commit()

            #try:
                # 使用execute方法执行SQL语句
            #    cursor.execute("insert into jobs values(" + jobDetail[0]+","+jobDetail[1]+","+ jobDetail[2]+","+ jobDetail[3]+","+ jobDetail[4].encode("utf-8") + ")")
                # 要提交
            #    db.commit()
            #except:
            #    print(u'插入失败')
            #    db.rollback()
        # 关闭游标
        cursor.close()
        # 关闭数据库连接
        db.close()



    def Start(self):
        self.enable = True
        page = self.page
        self.creatTable()
        while self.enable & (page < self.endPage):
            # 展示招聘信息
            self.showJob(page)
            self.writeTable(page)
            page += 1


print u'招聘内容：'
myModel = Spider_Model()
myModel.Start()