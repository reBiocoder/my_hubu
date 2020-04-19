"""
author:我爱小徐子
date:2018/11/13 23:17
"""
import requests
import json
from urllib import parse
from lxml import etree
import pymysql


class ZhihuSpiders(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    allColumnIdList = []
    eachColumnUrlList = []

    def allColumn(self, searchStr, offset):
        searchUrl = parse.quote(str(searchStr))
        allColumnUrl = "https://www.zhihu.com/api/v4/search_v3?t=column&q=" + str(
            searchUrl) + "&correction=1&offset=" + str(offset) + "&limit=10&show_all_topics=1"
        allColumnRes = requests.get(allColumnUrl, headers=self.headers)
        # 使用json转化为json格式
        allColumnResJson = json.loads(allColumnRes.text)
        # 得到paging中的信息，判断是否为最后一页
        allColumnPaging = allColumnResJson['paging']
        allColumnPagingIsEnd = allColumnPaging['is_end']
        if allColumnPagingIsEnd == False:
            allColumnResJsonData = allColumnResJson['data']
            # 计数器
            counter = 0
            for eachData in allColumnResJsonData:
                with  open(r'C:\Users\13016\Desktop\allColumn.txt', 'a+') as f:
                    f.write("{}\r\n".format(eachData['object']['id']))
                counter += 1
                self.allColumnIdList.append(eachData['object']['id'])  # 将id加入类属性中存储起来
            return int(counter)
        else:
            return 0

    def allColumnSpider(self):
        """
        调用allColumn函数得到具有该关键字的所有专栏id
        :return:
        """
        self.searchStr = "生物信息学"
        self.offset = 0
        allColumnRes = self.allColumn(self.searchStr, self.offset)
        try:
            n = 1
            while allColumnRes != 0:
                self.offset += allColumnRes
                allColumnRes = self.allColumn(self.searchStr, self.offset)
                n += 1
            return int(n)
        except:
            return 0

    #############################################
    # 在获取到id之后，对每个专栏中的文章url进行获取
    #############################################
    def eachColumn(self, eachColumnId, eachColumnOffset):
        """
        专栏api：https://zhuanlan.zhihu.com/api2/columns/专栏id/articles?limit=10&offset=0
        :return:
        """
        eachColumnUrl = "https://zhuanlan.zhihu.com/api/columns/" + str(
            eachColumnId) + "/articles?limit=10&offset=" + str(eachColumnOffset)
        eachColumnRes = requests.get(eachColumnUrl, headers=self.headers)
        eachColumnResJs = json.loads(eachColumnRes.text)
        eachColumnResIsEnd = eachColumnResJs['paging']['is_end']
        if eachColumnResIsEnd == False:
            n = 0
            for i in eachColumnResJs['data']:
                self.eachColumnUrlList.append(i['url'])
                n += 1
                return int(n)
        else:
            return 0

    def eachColumnSpider(self):
        counter = 0
        for eachColumnId in self.allColumnIdList:
            self.eachColumnOffset = 0
            eachColumnRes = self.eachColumn(eachColumnId, self.eachColumnOffset)
            n = 1
            while eachColumnRes != 0:
                self.eachColumnOffset += eachColumnRes
                eachColumnRes = self.eachColumn(eachColumnId, self.eachColumnOffset)
                n += 1
                counter += 1
                print("专栏id:{},正在进行第{}次爬取".format(eachColumnId, counter))


        return self.eachColumnUrlList

    ###################################
    # 得到文章内容，使用eachColumnSpiders
    # 得到的url列表
    ###################################

    def eachContent(self, contentUrl):
        contentRes = requests.get(contentUrl, headers=self.headers)
        contentResHtml = etree.HTML(contentRes.text).xpath("//script/text()")[1]
        contentResJs = json.loads(contentResHtml)
        contentResHtmlId = list(contentResJs['initialState']['entities']['articles'].keys())[0]
        name = contentResJs['initialState']['entities']['articles'][contentResHtmlId]['author']['name']
        title = contentResJs['initialState']['entities']['articles'][contentResHtmlId]['title'] + "(来源于知乎：" + str(
            name) + ")"
        content = contentResJs['initialState']['entities']['articles'][contentResHtmlId]['content']
        print("标题：",title)
        print("内容:",content)
        print("-------------------------------------------------------")
        """
        连接数据库
        """
        db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='ZPaixzh1314', db='my_hubu')
        cursor = db.cursor()
        sql = "insert into topic_create_topic_model(title,content,zhihu_id,draft_pk,pub_time,read_nums,pictureUrl,update_time,top,slug,agree,node_id,user_id)  values (%s,%s,'1',NULL ,'2019-03-03 14:57:21.016519',0,'无','2018-11-05 14:57:21.016519',0,%s,0,32,31)"
        post = [title, content,title]
        cursor.execute(sql, post)
        db.commit()
        db.close()
        return 1


    def eachContentSpider(self):
        allResultUrl = self.eachColumnSpider()
        print(allResultUrl[28],allResultUrl[29],allResultUrl[30])
        n = 0
        for eachUrl in allResultUrl:
            eachContentRes = self.eachContent(eachUrl)
            if eachContentRes != 0:
                n += 1
                print("正在存入第{}篇文章".format(n))
            else:
                break


if __name__ == "__main__":
    spider = ZhihuSpiders()
    res = spider.allColumnSpider()
    #spider.eachColumnSpider()
    spider.eachContentSpider()
